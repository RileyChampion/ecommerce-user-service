FROM "python:3.9-bullseye"

WORKDIR /app

COPY . .

RUN pip install -r ./requirements/dev.txt

EXPOSE 8000

CMD ["fastapi", "dev", "./app/main.py", "--host", "0.0.0.0", "--port", "8000"]