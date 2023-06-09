FROM python:3.10-bullseye

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY loansvc/ ./loansvc/
COPY utils/* .

CMD ["/app/init_server.sh"]