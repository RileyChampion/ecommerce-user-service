FROM "python:3.9-bullseye"

WORKDIR /app

COPY . .

RUN pip install -r ./requirements/prod.txt

EXPOSE 8000

CMD ["fastapi", "run", "./app/main.py", "--host", "0.0.0.0", "--port", "8000"]
