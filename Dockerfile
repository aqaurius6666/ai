
FROM python:3.6-stretch

# install build utilities
RUN apt-get update && \
    apt-get install -y gcc make apt-transport-https ca-certificates build-essential
RUN add-apt-repository ppa:ubuntugis/ppa 
RUN apt-get update
RUN apt-get install gdal-bin
RUN apt-get install libgdal-dev


ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

# check our python environment
RUN python3 --version
RUN pip3 --version

# set the working directory for containers
WORKDIR  /src

# Installing python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all the files from the project’s root to the working directory

# Running Python Application
CMD ["python3", "main.py"]
