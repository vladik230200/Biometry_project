# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt
# RUN apt install ffmpeg -y
RUN apt-get -y update && apt-get -y upgrade && apt-get install -y ffmpeg

WORKDIR /app
COPY . /app

RUN mkdir /app/biometry_main/temp

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "web_biometry.wsgi"]
CMD ["python", "biometry_main/manage.py", "runserver_plus", "--cert", "certname", "0.0.0.0:8000"]
