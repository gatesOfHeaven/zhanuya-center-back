FROM python:latest

# Set environment variables to prevent Python from writing .pyc files and to keep output unbuffered
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV LANG=C.UTF-8

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file first for more efficient caching
COPY requirements.txt ./

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application code to /back
COPY . .
# Expose the port (if needed for your application)
EXPOSE 2222

# Set the default command to run the application
CMD ["python", "main.py"]