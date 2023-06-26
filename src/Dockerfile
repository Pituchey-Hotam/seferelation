# Use the official Python base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements files to the working directory
COPY requirements.txt setup.py /app/

# Install the Python dependencies
RUN pip install -r requirements.txt

# Copy the source code to the working directory
COPY seferelation /app/seferelation

# Change the working directory to seferelation
WORKDIR /app/seferelation

# Run main.py to generate the graph-model.pickle file
RUN python main.py

# Change the working directory back to /app
WORKDIR /app

# Expose the port that the API will run on
EXPOSE 80

# Set the entrypoint command to start the API using uvicorn
CMD ["uvicorn", "apiserver:app", "--host", "0.0.0.0", "--port", "80", "--reload"]