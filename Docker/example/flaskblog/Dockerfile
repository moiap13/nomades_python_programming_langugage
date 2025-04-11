# For this container we want to use an ubuntu machine; 
# The same as the one used for the virtualbox virtual machine
FROM python:3.10-bookworm

# We create a working directory (main directory inside the container)
WORKDIR /app

# We copy the folder that containes our app inside the container
COPY ./flaskblog /app/flaskblog

# We expose the port 5050 
# -> this mean we want to use port 5050 of the container outside the container
# Here the port 5050 is the port used by flask
EXPOSE 8081

# We install the requirements for python
# The requirements.txt contains all the dependencies we need to run the app properly
RUN pip install -r flaskblog/requirements.txt

# We run the app, as the default command
CMD ["python3.10", "flaskblog/app.py"]