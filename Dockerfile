FROM python:3.10-slim

COPY bot.py /app/
COPY requirements.txt /app/
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "bot.py" ]
