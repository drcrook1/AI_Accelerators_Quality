FROM continuumio/miniconda3

RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install curl -y

RUN apt-get install build-essential libssl-dev libffi-dev unixodbc-dev -y

RUN pip install --upgrade pip setuptools wheel

RUN conda install psutil -y

# Install PyODBC PreReqs
RUN apt-get install apt-transport-https ca-certificates -y
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/9/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update -y
RUN ACCEPT_EULA=Y apt-get install msodbcsql17 -y
# End install PyODBC PreReqs

ADD requirements.txt /app/
RUN pip install -r /app/requirements.txt

EXPOSE 80

COPY . /webapp/

RUN mv /webapp/run.py /run.py

RUN chmod -x /run.py

ENV PYTHONUNBUFFERED 1

CMD ["python", "/run.py"]
#CMD ["gunicorn", "-b", "0.0.0.0:80", "-w", "1", "run:app"]