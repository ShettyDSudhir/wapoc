# set base image (host OS)
FROM python:3.10-slim

#Make a 
# set the working directory in the container
WORKDIR /code

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
#RUN pip install flask pika gunicorn
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY . .

# command to run on container start
CMD [ "python3", "./wsgi.py" ]
#ENTRYPOINT ["./gunicorn.sh"]