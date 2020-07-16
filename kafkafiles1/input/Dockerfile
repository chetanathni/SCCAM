FROM python:3.6
RUN pip install kafka 
COPY ./ /app
#CMD ["python3","-u","/app/producer1.py"]
CMD ["python3","-u","/app/send.py"]