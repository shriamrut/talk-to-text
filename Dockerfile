# Use the official Python image as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /talk-to-text

# Copy the requirements file into the container at /talk-to-text
COPY requirements.txt .

# Install any dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Download models for LLM from hugging face
RUN python3 llm/pre-requisite.py

# Expose port 8000 to allow communication to the FastAPI application
EXPOSE 8000

# Command to run the FastAPI server with Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

