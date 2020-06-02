FROM python:3.7-alpine
WORKDIR /app
RUN apk update && \
    apk add --virtual build-deps gcc python-dev musl-dev && \
    apk add postgresql-dev
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

ENTRYPOINT [ "python" ]
CMD ["gen_upload.py"]