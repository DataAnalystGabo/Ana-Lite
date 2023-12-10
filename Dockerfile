FROM python:3.10
WORKDIR /analite
COPY requirements.txt /analite/
RUN pip install -r requirements.txt
COPY . /analite
CMD python /analite/src/main.py