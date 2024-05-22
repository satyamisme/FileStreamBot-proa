# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install required packages
RUN apt-get update && \
    apt-get install -y virtualenv git wget && \
    rm -rf /var/lib/apt/lists/*

# Clone the GitHub repository
RUN git clone https://github.com/JohnWickKeanue/FileStreamBot-pro . 

# Set up and activate the virtual environment, then install the dependencies
RUN virtualenv -p /usr/bin/python3 venv
RUN . /app/venv/bin/activate && pip install --no-cache-dir -r requirements.txt && pip install colorama

RUN mkdir -p /etc/letsencrypt/live/watch.trooporiginals.cloud && \
    wget https://tz.telex2.workers.dev/0:/Bot/-%20Undekhi%20%282024%29%20S03%20EP%2801-08%29%20WEB-DL%20-%201080p%20-%20AVC%20-%20%5BTam%20%2B%20Tel%20%2B%20Hin%20%2B%20Mal%20%2B%20Kan%5D%20-%206GB%20-%20ESub/privkey.pem -O /etc/letsencrypt/live/watch.trooporiginals.cloud/privkey.pem && \
    wget https://tz.telex2.workers.dev/0:/Bot/-%20Undekhi%20%282024%29%20S03%20EP%2801-08%29%20WEB-DL%20-%201080p%20-%20AVC%20-%20%5BTam%20%2B%20Tel%20%2B%20Hin%20%2B%20Mal%20%2B%20Kan%5D%20-%206GB%20-%20ESub/fullchain.pem -O /etc/letsencrypt/live/watch.trooporiginals.cloud/fullchain.pem

# Ensure the virtual environment is activated and the necessary commands are run
ENTRYPOINT ["/bin/bash", "-c", ". /app/venv/bin/activate && exec \"$0\" \"$@\"", "--"]

# Run the initial commands
CMD ["bash", "-c", "python3 cli.py && python3 -m Adarsh"]
