FROM python:3.6
RUN pip install kafka 
RUN pip install pymongo
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.7.3/wait /wait
RUN chmod +x /wait
COPY ./ /app
#CMD ["python3","-u","/app/producer1.py"]
CMD ["/wait","python3","-u","/app/send.py"]
