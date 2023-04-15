FROM python:3.8.10

ENV REDIS_IP redis-db

RUN pip install Flask==2.2.0 
RUN pip install redis==4.5.1 
RUN pip install requests==2.22.0
RUN pip install numpy==1.24.2
RUN pip install matplotlib==3.7.1


ADD ./autoTrendsData.csv /autoTrendsData.csv
ADD ./autoTrends_app.py /autoTrends_app.py

CMD ["python", "/autoTrends_app.py"]