# Automotive CO2 Emissions and Fuel Economy Information
The purpose of this project is to query and return interesting information from the EPA (Environmental Protection Agency) and NHTSA (National Highway Traffic Safety Administration) about the automotive industry’s CO2 emissions and fuel economy. This information is critical to the sustainability of transportation as concerns of climate change and environmental pollution rise.

## Retrieve Data

The user may view the website that the CO2 Emissions and Fuel Economy data comes from using the link below:

```bash
https://www.epa.gov/automotive-trends/explore-automotive-trends-data #DetailedData
```
The data can be downloaded in ``CSV`` format. Please note that there is not a live link to CSV file, the user must save the file on his/her workspace in the same folder as this project.

## Installation

To begin, make a new folder for this project. An example is shown below:
```console
[user-vm]$ cd ~/coe-332/
[user-vm]$ mkdir redis/
[user-vm]$ cd redis/
[user-vm]$ pwd
/home/ubuntu/coe332/redis
```
Install this project by cloning the repository, making the scripts executable, and adding them to your PATH. For example:

```bash
git clone ssh://git@github.com:alb6443/COE332-homeworks.git <directory>
```
This project lives within the ``homework07`` folder.

## Getting started
### Build a new image via Dockerfile
To start the Flask app, you can find a couple helpful commands below:
```console
[user-vm]$ docker-compose up --build      % Start the services and build the docker image
[user-vm]$ docker ps -a     % Check if image is up
[user-vm]$ docker-compose down      % Kill the services
[user-vm]$ docker ps -a     % Check if image is exited
```
### Pull existing image via Docker Hub
Install this project by pulling the image from Docker Hub. Execute the following lines:
```console
[user-vm]$ docker pull alb6443/auto_trends_app:hw06
[user-vm]$ docker run -it --rm -p 5000:5000 alb6443/auto_trends_app:hw06
 * Serving Flask app 'auto_trends_app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 434-637-715
```
You now have access to all of the routes detailed below. For more information, [go to Make a Request section](#make-a-request).

### Kubernetes 
Install this project by cloning the repository, making the scripts executable, and adding them to your PATH. For example:

```bash
git clone ssh://git@github.com:alb6443/COE332-homeworks.git <directory>
```
This project lives within the ``homework07`` folder.

If you build your own image as instructed in Build a new image via Dockerfile, push the image to DockerHub with the following command:

```bash
docker push <username>/auto_trends_app:hw07
```
Once your image is pushed to DockerHub, construct ``<username>-test-flask-deployment.yml``.

```bash
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: alb6443-test-flask-deployment
  labels:
    app: alb6443-test-flask-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: alb6443-test-flask-app
  template:
    metadata:
      labels:
        app: alb6443-test-flask-app
    spec:
      containers:
        - name: alb6443-test-flask-app
          imagePullPolicy: Always
          image: <username>/auto_trends_app:hw07
          env:
          - name: REDIS_IP
            value: 10.233.34.143
          ports:
          - name: http
            containerPort: 5000
```
Next, apply the pvc by using the following command:

```bash
kubectl apply -f alb6443-test-redis-pvc.yml
```
We create a deployment in k8s using the apply command, just like when creating a pod:
```bash
kubectl apply -f alb6443-test-deployment-pvc.yml
```

Lastly, to set up Redis, apply the service file:
```bash
kubectl apply -f alb6443-test-redis-service.yml
```

Once you've applied the three ``.yml`` files mentioned, ensure that the proper IP addresses are connected. Preform the following command:
```console
alb6443@kube-access:~/COE332-homeworks/homework07$ kubectl get services
NAME                         TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
alb6443-test-redis-service   ClusterIP   10.233.34.143   <none>        6379/TCP   6d20h
```
Identify the IP address and replace the existing IP address within ``alb6443-test-deployment-pvc.yml`` with the proper IP address that you identified under CLUSTER-IP.

Once Redis is set up, it's time to set up the Flask service. The procedure is the same but with the Flask ``deployment.yml`` and ``service.yml``.

```bash
kubectl apply -f alb6443-test-flask-deployment.yml
kubectl apply -f alb6443-test-flask-service.yml
```
Once you've applied the two ``.yml`` files mentioned, ensure that the proper IP addresses are connected. Preform the following command:
```console
alb6443@kube-access:~/COE332-homeworks/homework07$ kubectl get services
NAME                         TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
alb6443-test-flask-service   ClusterIP   10.233.42.109   <none>        6379/TCP   6d20h
```
Identify the IP address and use that IP address when performing curl commands. For example, if the CLUSTER-IP is 10.233.42.109, the command would look like such:
```bash
curl 10.233.42.109:5000/<route>
```

## Understanding the Scripts

This project has one script-- ``autoTrends_app.py``

**``autoTrends_app.p``**: This script is a Flask application that has three routes: ``/data``, ``/years``, and ``/years/<year>``. The routes are explained in further detail below:

### Make a Request
Open a separate terminal window for the next step. Make sure the services are up and running with the previously mentioned ``run`` command. To make a request to your Flask app, type the following in the new terminal:

```console
[user-vm]$ curl 10.233.42.109:5000/data -X POST
```
All of the data from the automotive trends file will populate. To retrieve other data, familiarize yourself with the other routes detailed in the table below:

<table>
<tr>
<td> Route </td> <td> Description and output</td>
</tr>
<tr>
<td> <code>/data -X POST</code> </td>
<td>

The entire data set will be loaded into the database
```console
data loaded into Redis
```
</td>

</tr>
<tr>
<td> <code>/data</code> </td>
<td>

A list of all information in the data set will show

```json 
... {
    "2-Cycle MPG": "14.38083",
    "4 or Fewer Gears": "-",
    "5 Gears": "-",
    "6 Gears": "-",
    "7 Gears": "-",
    "8 Gears": "-",
    "9 or More Gears": "-",
    "Acceleration (0-60 time in seconds)": "-",
    "Average Number of Gears": "-",
    "Cylinder Deactivation": "-",
    "Drivetrain - 4WD": "-",
    "Drivetrain - Front": "-",
    "Drivetrain - Rear": "1.000",
    "Engine Displacement": "305.7401",
    "Footprint (sq. ft.)": "-",
    "Fuel Delivery - Carbureted": "1.000",
    "Fuel Delivery - Gasoline Direct Injection (GDI)": "-",
    "Fuel Delivery - Other": "-",
    "Fuel Delivery - Port Fuel Injection": "-",
    "Fuel Delivery - Throttle Body Injection": "-",
    "HP/Engine Displacement": "0.442154",
    "HP/Weight (lbs)": "0.032524",
    "Horsepower (HP)": "136.0330",
    "Manufacturer": "GM",
    "Model Year": "1975",
    "Multivalve Engine": "-",
    "Powertrain - Diesel": "-",
    "Powertrain - Electric Vehicle (EV)": "-",
    "Powertrain - Fuel Cell Vehicle (FCV)": "-",
    "Powertrain - Gasoline": "1.000",
    "Powertrain - Gasoline Hybrid": "-",
    "Powertrain - Other (incl. CNG)": "-",
    "Powertrain - Plug-in Hybrid Electric Vehicle (PHEV)": "-",
    "Production (000)": "124",
    "Production Share": "0.012",
    "Real-World CO2 (g/mi)": "727.65849",
    "Real-World CO2_City (g/mi)": "763.15752",
    "Real-World CO2_Hwy (g/mi)": "684.27078",
    "Real-World MPG": "12.21315",
    "Real-World MPG_City": "11.64504",
    "Real-World MPG_Hwy": "12.98755",
    "Regulatory Class": "Truck",
    "Stop/Start": "-",
    "Ton-MPG (Real-World)": "26.27661",
    "Transmission - Automatic": "0.764",
    "Transmission - CVT (Hybrid)": "-",
    "Transmission - CVT (Non-Hybrid)": "-",
    "Transmission - Lockup": "-",
    "Transmission - Manual": "0.236",
    "Transmission - Other": "-",
    "Turbocharged Engine": "-",
    "Variable Valve Timing": "-",
    "Vehicle Type": "Minivan/Van",
    "Weight (lbs)": "4183.422"
    },
  ...
```

</td>
</tr>

<tr>
<td> <code>/data -X DELETE </code> </td>
<td>

Deletes all data from the data base

``` 
data deleted, there are 0 keys in the db
```
</td>
</tr>

<tr>
<td> <code>/years </code> </td>
<td>

Comprehensive list of all of the years that the automotive trends data has        

```
[
  "2006",
  "1978",
  "2005",
  "1998",
  "1987",
  "2000",
  "2014",
  "1989",
  "1976",
  "1981",
  "2011",
  "2013",
  "1993",
  "1985",
  "1977",
  "1979",
  "2008",
  "2003",
  "2017",
  "1991",
  "2004",
  "1975",
  "2019",
  "1980",
  "1988",
  "1997",
  "2018",
  "1983",
  "1986",
  "1995",
  "1999",
  "Prelim. 2022",
  "1984",
  "1982",
  "2021",
  "2015",
  "1992",
  "2016",
  "1994",
  "1990",
  "2002",
  "2012",
  "1996",
  "2007",
  "2010",
  "2001",
  "2020",
  "2009"
]
```

</td>
</tr>

<tr>
<td> <code>/years/&ltyear&gt </code> </td>
<td>

Return all information about the cars found in the specified year

``` 
...
{
    "2-Cycle MPG": "32.62186",
    "4 or Fewer Gears": "0.018",
    "5 Gears": "0.008",
    "6 Gears": "0.173",
    "7 Gears": "0.021",
    "8 Gears": "0.288",
    "9 or More Gears": "0.212",
    "Acceleration (0-60 time in seconds)": "7.7922",
    "Average Number of Gears": "6.9",
    "Cylinder Deactivation": "0.147",
    "Drivetrain - 4WD": "0.499",
    "Drivetrain - Front": "0.406",
    "Drivetrain - Rear": "0.094",
    "Engine Displacement": "169.5194",
    "Footprint (sq. ft.)": "50.91736",
    "Fuel Delivery - Carbureted": "-",
    "Fuel Delivery - Gasoline Direct Injection (GDI)": "0.571",
    "Fuel Delivery - Other": "0.022",
    "Fuel Delivery - Port Fuel Injection": "0.406",
    "Fuel Delivery - Throttle Body Injection": "-",
    "HP/Engine Displacement": "1.502554",
    "HP/Weight (lbs)": "0.057810",
    "Horsepower (HP)": "245.8668",
    "Manufacturer": "All",
    "Model Year": "2020",
    "Multivalve Engine": "0.907",
    "Powertrain - Diesel": "0.005",
    "Powertrain - Electric Vehicle (EV)": "0.018",
    "Powertrain - Fuel Cell Vehicle (FCV)": "0.000",
    "Powertrain - Gasoline": "0.924",
    "Powertrain - Gasoline Hybrid": "0.049",
    "Powertrain - Other (incl. CNG)": "-",
    "Powertrain - Plug-in Hybrid Electric Vehicle (PHEV)": "0.005",
    "Production (000)": "13721",
    "Production Share": "1.000",
    "Real-World CO2 (g/mi)": "348.76917",
    "Real-World CO2_City (g/mi)": "404.24868",
    "Real-World CO2_Hwy (g/mi)": "306.91621",
    "Real-World MPG": "25.38325",
    "Real-World MPG_City": "21.91254",
    "Real-World MPG_Hwy": "28.82778",
    "Regulatory Class": "All",
    "Stop/Start": "0.458",
    "Ton-MPG (Real-World)": "56.64466",
    "Transmission - Automatic": "0.027",
    "Transmission - CVT (Hybrid)": "0.028",
    "Transmission - CVT (Non-Hybrid)": "0.250",
    "Transmission - Lockup": "0.683",
    "Transmission - Manual": "0.011",
    "Transmission - Other": "-",
    "Turbocharged Engine": "0.347",
    "Variable Valve Timing": "0.958",
    "Vehicle Type": "All",
    "Weight (lbs)": "4166.247"
  },
  ...
```
</td>
</tr>
</table>

To access the other routes, append it to the command previously mentioned in [Make a Request](#make-a-request).
