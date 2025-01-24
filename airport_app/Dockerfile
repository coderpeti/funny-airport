# Python3 is used from a docker image
FROM python:3

# Import of all files into the container
COPY . /usr/src/app
# The working directory will be the container
WORKDIR /usr/src/app
# Install all dependencies into the container
RUN pip install -r requirements.txt
# Runs when I run the container
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]