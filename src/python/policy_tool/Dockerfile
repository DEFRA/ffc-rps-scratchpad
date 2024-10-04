# Use the official Python image from Docker Hub
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Set the PYTHONPATH to the /app directory
ENV PYTHONPATH=/app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application into the container
COPY app .

# Expose the port that FastAPI will run on
EXPOSE 8000

# Command to run the FastAPI application
#CMD ["uvicorn", "app.alb_checker_api:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["fastapi", "run", "alb_checker_api.py", "--port", "8000"]
#CMD bash