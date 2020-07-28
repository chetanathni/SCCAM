FROM python:3.6
RUN pip install kafka  
RUN pip install dash-bootstrap-components
RUN pip install dash
RUN pip install dash_daq
COPY ./ /app
EXPOSE 8050
CMD ["python","-u","/app/consumer1.py"]
