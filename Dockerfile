FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./app ./app


# Expose the port FastAPI/uvicorn will run on
EXPOSE 8000

# Command to run when container starts
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

