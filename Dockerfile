FROM python:3.11-alpine as builder

WORKDIR /app

COPY requirements.txt .

RUN apk add gcc python3-dev musl-dev

RUN python -m venv /app/venv

ENV PATH="/app/venv/bin:$PATH"

RUN pip install -r requirements.txt

FROM python:3.11-alpine

RUN addgroup app_user --gid 1000 && adduser -S app_user -u 1000 -G app_user

WORKDIR /app

ENV PATH="/app/venv/bin:$PATH"

RUN apk update \
	&& apk -U upgrade \
	&& apk add --no-cache ca-certificates \
    && update-ca-certificates --fresh \
	&& rm -rf /var/cache/apk/*

COPY --from=builder /app/venv /app/venv
COPY --chown=app_user:app_user . .

USER app_user

ENTRYPOINT ["python3", "main.py"]