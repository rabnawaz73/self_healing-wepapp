FROM public.ecr.aws/lambda/python:3.12

WORKDIR /var/task

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

ENV APP_VERSION=1.0
ENV ENVIRONMENT=production
ENV FORCE_UNHEALTHY=false

CMD ["app.main.handler"]
