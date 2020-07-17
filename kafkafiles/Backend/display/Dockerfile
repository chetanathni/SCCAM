FROM python:3
WORKDIR /app
RUN pip install kafka
RUN pip install pymongo
COPY . .
CMD ["python","-u","display.py"]
