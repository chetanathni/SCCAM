FROM python:3.6
WORKDIR /app
RUN pip install kafka  
RUN pip install pymongo
COPY . .
CMD ["python","-u","producer.py"]
