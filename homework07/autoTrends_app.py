from flask import Flask, request
import requests
import json
import redis
import csv
import os
import numpy as np
import matplotlib.pyplot as plt

app = Flask(__name__)

def get_redis_client():
    """
    Initialize Redis client to that allows redis to communicate with flask and docker
    Args:
        N/A
    Returns:
        Redis client
    """
    return redis.Redis(host=os.getenv('REDIS_IP','redis-db'), port=6379, db=0, decode_responses = True)

rd = get_redis_client()

@app.route('/data', methods=['POST','GET','DELETE'])
def handle_data():
    """
    This function has 3 capabilities:
        1. shows all of the data
        2. loads all of the data
        3. deletes all of the data
    Args:
        N/A
    Returns:
        outputList (list): all of the data within the database as a list
        str: Command status that tells user if command was successful or not.
    """
    if request.method == 'GET':
        outputList = []
        for item in rd.keys():
            outputList.append(rd.hgetall(item))
        return outputList

    elif request.method == 'POST':
        with open('autoTrendsData.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                item = dict(row)
                key = f'{item["Manufacturer"]}:{item["Model Year"]}:{item["Vehicle Type"]}'
                rd.hset(key, mapping = item)
        return 'data loaded into Redis\n'

    elif request.method == 'DELETE':
        rd.flushdb()
        return f'data deleted, there are {len(rd.keys())} keys in the db\n'

    else:

        return 'The method you tried does not work\n'

@app.route('/years', methods=['GET'])
def showYears() -> list:
    """
    Returns a comprehensive list of all the unique years within the dataset
    Args:
        N/A
    Returns:
        compList (list): All Model Years within the data set from the AutoTrends data as a comprehensive list
    """
    if len(rd.keys()) == 0:
        return 'No data in db. Post data to get info\n'
    allYears = []
    for key in rd.keys():
        carDict = rd.hgetall(key)
        allYears.append(carDict['Model Year'])
    compList = [*set(allYears)]
    return compList

@app.route('/years/<year>', methods=['GET'])
def showCars(year: str) -> list:
    """
    Retrievs all data from a specified year
    Args:
        year (str): A specific year the user wants to identify all automotive trend data
    Returns:
        yearInfo (list): list with cars from the specified year, if year not found, will be empty list
    """
    if len(rd.keys()) == 0:
        return 'No data in db. Post data to get info\n'
    yearInfo = []
    if year in showYears():
        for key in rd.keys():
            carDict = rd.hgetall(key)
            if carDict['Model Year'] == year:
                yearInfo.append(carDict)
    return yearInfo

@app.route('/plot', methods=['GET'])
def showPlot():
    """
    xxxxx
    Args:
        N/A
    Returns:
        xxxxx
    """
    x = np.linspace(0, 2 * np.pi, 50)
    plt.plot(x, np.sin(x), 'r-x', label='Sin(x)')
    plt.plot(x, np.cos(x), 'g-^', label='Cos(x)')
    plt.legend() # Display the legend.
    plt.xlabel('Rads') # Add a label to the x-axis.
    plt.ylabel('Amplitude') # Add a label to the y-axis.
    plt.title('Sin and Cos Waves') # Add a graph title.
    plt.savefig('/data/my_labels_legends.png')
    plt.show()
    # # read the raw file bytes into a python object
    file_bytes = open('/data/my_labels_legends.png', 'rb').read()

    # # set the file bytes as a key in Redis
    rd.set('key', file_bytes)

    if len(file_bytes) == 0:
        return 'No data in db. Post data to get info\n'
    else:
        return 'Plot is loaded.'
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
