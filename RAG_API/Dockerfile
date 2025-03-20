 # Use the smallest possible Python image (based on Alpine Linux)
 FROM python:3.9-slim
 # Set the working directory inside the container
 WORKDIR /app
 # Copy the requirements file into the container
 COPY requirements.txt /app/
 # Install the dependencies
 RUN pip install -r requirements.txt
 # Copy the rest of the app files into the container
 COPY . /app/
 # Expose the port that Fast api will run on
 EXPOSE 8000
 # Run the Flask app
 CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]