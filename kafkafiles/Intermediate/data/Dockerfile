FROM python:3.6
WORKDIR /app
RUN pip install kafka 
RUN pip install psutil
COPY . .
#CMD ["python3","-u","/app/producer1.py"]
CMD ["python3","-u","data.py"]