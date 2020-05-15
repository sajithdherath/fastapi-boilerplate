FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY api /app/app

ADD requirements.txt requirements.txt

RUN python3.7 -m pip install --no-cache-dir -r requirements.txt \
    && rm -rf ~/.cache/pip

