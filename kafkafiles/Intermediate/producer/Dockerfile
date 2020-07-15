FROM python:3.6
RUN pip install kafka  
COPY ./ /app
CMD ["python","-u","/app/producer.py"]
