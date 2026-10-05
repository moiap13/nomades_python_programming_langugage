FROM python:3.11-slim

WORKDIR /app

COPY app.py ./
COPY pages pages/

RUN pip install --no-cache-dir streamlit pandas matplotlib plotly wonderwords

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0", "--server.port", "8501"]