FROM python:3.9-slim-buster
RUN git clone https://github.com/JohnWickKeanue/FileStreamBot-pro
RUN cd FileStreamBot-pro
CMD ["bash", "script.sh"]
