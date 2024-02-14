FROM python:3.11

ENV TZ=America/Buenos_Aires
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

EXPOSE 8000

WORKDIR /code/

RUN pip install --upgrade pip

COPY ./requirements.txt /code/requirements.txt
COPY ./app /code/

RUN pip install -r /code/requirements.txt
 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
