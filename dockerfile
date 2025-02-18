FROM python:3.10-slim
ENV TOKEN="7706552456:AAHnWE2gkq5BsbVUhDx7IWtDqb_oDvf5vdQ"
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT [ "python", "bot.py" ]