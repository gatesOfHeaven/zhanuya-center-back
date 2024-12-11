# Use the official Python image from the Docker registry
FROM python:latest

# Set environment variables to prevent Python from writing bytecode and to ensure unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV LANG C.UTF-8

# Set the working directory inside the container
WORKDIR /back

# Copy the requirements file to the working directory in the container
COPY requirements.txt /back/

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /back/

# Expose port 2222
EXPOSE 2222

# Command to run the FastAPI app
CMD ["python", "main.py"]

