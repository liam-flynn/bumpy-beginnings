FROM python:3.10.12

# help from https://medium.com/@minghz42/docker-setup-for-django-on-mysql-1f063c9d16a0
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY . /app/

COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 8000

# make the entrypoint script executable
RUN chmod +x entrypoint.sh

# run the entrypoint script
CMD ["/bin/sh", "-c", "./entrypoint.sh"]