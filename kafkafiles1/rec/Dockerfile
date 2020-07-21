FROM python:3.6
WORKDIR /app
RUN pip install kafka  
COPY . .
CMD ["python","-u","/app/producer.py"]