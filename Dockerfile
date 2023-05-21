FROM python:3.11

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./financial /code/financial
COPY ./get_raw_data.py /code/

CMD ["uvicorn", "financial.main:app", "--host", "0.0.0.0", "--port", "80"]