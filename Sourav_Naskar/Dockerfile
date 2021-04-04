FROM python:3.8-slim-buster

# This prevents Python from writing out pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# This keeps Python from buffering stdin/stdout
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update \
    && apt-get -y install gcc make \
    && rm -rf /var/lib/apt/lists/*

# install dependencies
RUN pip install torch==1.6.0+cpu torchvision==0.7.0+cpu -f https://download.pytorch.org/whl/torch_stable.html
RUN pip install --no-cache-dir --upgrade pip

# set work directory
WORKDIR /src/app/flask_app
COPY . .

# install project requirements
RUN pip install --no-cache-dir -r requirements.txt

RUN ls -la /src/app/flask_app/

ENTRYPOINT python app.py