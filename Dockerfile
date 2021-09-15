FROM python:3.9-alpine

WORKDIR /code

COPY ./requirements.txt .

RUN python -m pip install --upgrade pip && pip install -r requirements.txt

COPY . .

RUN python3 manage.py collectstatic --noinput

RUN python manage.py makemigrations && python manage.py migrate

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
