FROM public.ecr.aws/docker/library/alpine:3.18.2

# setup python
ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

# setup pyenv
RUN apk add bash bash-doc bash-completion curl git build-base
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN curl https://pyenv.run | bash
ENV PATH $PATH:/root/.pyenv/bin

WORKDIR /code

COPY ./yurucamp /code

RUN python3 -m pip install pipenv

RUN pipenv install

ENTRYPOINT ["./start_backend.sh"]
