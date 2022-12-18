# 1. cd a la carpeta del proyecto
# 2. sudo docker build -t createhub_imagine:v1 .

# HUBI DISCORD IMAGE
FROM python:3.10-slim
LABEL maintainer="flowese <flowese@gmail.com>"
EXPOSE 5100
# Install ffmpeg
RUN apt-get update && apt install -y git
RUN apt-get install make -y
# Copy APP
COPY . /CreateHub_Imagine
WORKDIR /CreateHub_Imagine
# Copy and install requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["python", "src/app.py"]