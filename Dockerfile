FROM python:3.13-slim

WORKDIR /app

COPY . /app/

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir uv

RUN uv venv /app/venv

RUN /app/venv/bin/python -m ensurepip && \
    /app/venv/bin/pip install --upgrade pip

RUN /app/venv/bin/pip install -r requirements.txt

EXPOSE 8501

CMD ["sh", "-c", "streamlit run server.py"]
