# set base image (host OS)
FROM python:3.10

# set the working directory in the container
WORKDIR /recomb

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local schema to the working directory
COPY db/schema.sql db/schema.sql

# copy the content of the local src directory to the working directory
COPY src/ src/

# command to run on container start
CMD [ "python", "./src/service.py" ]
