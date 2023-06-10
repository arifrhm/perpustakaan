FROM python:3.9-alpine
# Install additional dependencies
RUN apk add --no-cache gcc musl-dev python3-dev libffi-dev openssl-dev cargo postgresql-dev postgresql-client
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN mkdir /app/migrations
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]