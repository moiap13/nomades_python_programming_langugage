# For this container we want to use an ubuntu machine; 
# The same as the one used for the virtualbox virtual machine
FROM python:3.12

# We install some dependencies such as python and pip
# RUN apt update -y \
#   && apt install software-properties-common -y \
#   && add-apt-repository ppa:deadsnakes/ppa \
#   && apt install python3.10 pip -y

# We create a working directory (main directory inside the container)
WORKDIR /app

# We copy the folder that containes our app inside the container
COPY ./flaskblog_v0.0.1 /app/flaskblog

# We expose the port 8080 
# -> this mean we want to use port 8080 of the container outside the container
# Here the port 8080 is the port used by flask
EXPOSE 8080

# We install the requirements for python
# The requirements.txt contains all the dependencies we need to run the app properly
RUN pip install -r flaskblog/requirements.txt

# We run the app, as the default command
CMD ["python3.12", "flaskblog/app.py"]