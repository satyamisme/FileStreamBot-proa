# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install required packages
RUN apt-get update && \
    apt-get install -y virtualenv git && \
    rm -rf /var/lib/apt/lists/*

# Clone the GitHub repository
RUN git clone https://github.com/JohnWickKeanue/FileStreamBot-pro . 

# Set up and activate the virtual environment, then install the dependencies
RUN virtualenv -p /usr/bin/python3 venv
RUN . /app/venv/bin/activate && pip install --no-cache-dir -r requirements.txt && pip install colorama

# Ensure the virtual environment is activated and the necessary commands are run
ENTRYPOINT ["/bin/bash", "-c", ". /app/venv/bin/activate && exec \"$0\" \"$@\"", "--"]

# Run the initial commands
CMD ["bash", "-c", "python3 cli.py && python3 -m Adarsh"]
