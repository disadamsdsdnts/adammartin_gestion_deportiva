FROM adammartin/django_base

ENV PYTHONUNBUFFERED 1

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install -r /requirements/dev.txt

COPY ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r//' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/dev/django/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start

WORKDIR /app

ENTRYPOINT ["/entrypoint"]
