FROM python:3.9-alpine

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# create root directory for our project in the container
RUN mkdir /vendor_management_system

WORKDIR /vendor_management_system

# copy current directory contents into the container at /vendor_management_system
ADD . /vendor_management_system/

# install required packages
RUN pip install -r requirements.txt