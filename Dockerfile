FROM python:3.13-slim

WORKDIR /app

COPY . /app/

RUN pip install --no-cache-dir uv

RUN uv pip install --system -r requirements.txt

EXPOSE 8501

CMD ["sh", "-c", "streamlit run server.py"]
