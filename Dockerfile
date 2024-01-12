FROM ghcr.io/coqui-ai/tts

# CPU only? Use base image below
# FROM ghcr.io/coqui-ai/tts-cpu 

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip3 install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./main.py /code/
VOLUME ["/audio"]

EXPOSE 7861 
ENTRYPOINT yes | uvicorn main:app --host "0.0.0.0" --port "7861"