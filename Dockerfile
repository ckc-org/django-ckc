FROM python:3.9.2

# Spatial packages and such
RUN apt-get update && apt-get install -y libgdal-dev libsqlite3-mod-spatialite

# Python reqs
ADD requirements.txt .
RUN pip install -r requirements.txt

# add all of our source + config
ADD ckc/ /src/ckc/
ADD testproject/ /src/testproject
ADD tests/ /src/tests
ADD setup.cfg /src
WORKDIR /src
