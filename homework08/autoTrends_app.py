from flask import Flask, request, send_file
import requests
import json
import redis
import csv
import os
import numpy as np
import matplotlib.pyplot as plt

app = Flask(__name__)

redis_ip = os.environ.get('REDIS_IP')
if not redis_ip:
    raise Exception()
rd=redis.Redis(host=redis_ip, port=6379, db=0, decode_responses=True)
rd1=redis.Redis(host=redis_ip, port=6379, db=1)

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

@app.route('/image', methods=['GET'])
def showPlot():
    """
    xxxxx
    Args:
        N/A
    Returns:
        Returns a plot of the 2021 MPG vs car type.
    """
    # x = np.linspace(0, 2 * np.pi, 50)
    # plt.plot(x, np.sin(x), 'r-x', label='Sin(x)')
    # plt.plot(x, np.cos(x), 'g-^', label='Cos(x)')
    # plt.legend() # Display the legend.
    # plt.xlabel('Rads') # Add a label to the x-axis.
    # plt.ylabel('Amplitude') # Add a label to the y-axis.
    # plt.title('Sin and Cos Waves') # Add a graph title.
    # plt.savefig('/data/my_labels_legends.png')
    # plt.show()
    # # # read the raw file bytes into a python object
    # file_bytes = open('/data/my_labels_legends.png', 'rb').read()
    if request.method == 'POST':
        if len(rd.keys()) == 0:
            return 'No data in db. Post data to get info\n'
        else:
            x = []
            y = []    

            allYears = []
            for key in rd.keys():
                carDict = rd.hgetall(key)
                allYears.append(carDict['Model Year'])

            if allYears == '2021':
                year = float(allYears)
                mpg = rd.hget(key, 'Real-World MPG')
                carType = rd.hget(key, 'Vehicle Type')
                if mpg != '-':
                    x.append(carType)
                    y.append(float(mpg))
                    
            plt.bar(x, y, color = 'g', width = 0.72, label = "MPG")
            plt.xlabel('Vehicle Type')
            plt.ylabel('MPG')
            plt.title('2021: MPG vs Vehicle Type')
            plt.legend()
            plt.savefig('./data/2021_MPGvType.png')
            file_bytes = open('./data/2021_MPGvType.png', 'rb').read()
            # set the file bytes as a key in Redis
            rd1.set('plot', file_bytes)
            if len(file_bytes) == 0:
                return 'No data in db. Post data to get info\n'
            else:
                return 'Plot is loaded.'

    elif request.method == 'GET':
        if redis.exists('plot'):
            path = './data/2021_MPGvType.png'
            with open(path, 'wb') as f:
            #get the image based on the 'plot' and write that binary stream to the
            #file path
                f.write(rd1.get('plot'))
            return send_file(path, mimetype='image/png', as_attachment=True)
        else: 
            return 'Plot not found\n'
    
    elif request.method == 'DELETE':
        if rd1.exists('plot'):
            rd1.flushdb()
            return 'Plot has been deleted\n'
        else:
            return 'The method you tried does not work. DB already empty\n'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
