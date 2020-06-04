FROM python:3.7-alpine
WORKDIR /app
# Installing client libraries and any other package you need
RUN apk update && apk add libpq

# Installing build dependencies
# For python3 you need to add python3-dev *please upvote the comment
# of @its30 below if you use this*
RUN apk add --virtual .build-deps gcc python3-dev musl-dev postgresql-dev

RUN pip install psycopg2

# Delete build dependencies
RUN apk del .build-deps
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

ENTRYPOINT [ "python" ]
CMD ["gen_upload.py"]