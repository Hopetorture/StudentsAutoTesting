FROM python:3.7.2-stretch
ADD judge.py /

# RUN pip install numpy
RUN apt-get update
RUN apt-get install build-essential

ENTRYPOINT [ "python", "./judge.py" ]
