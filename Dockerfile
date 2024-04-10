FROM python:3.11-slim

COPY ./requirements.txt ./

RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN useradd -m -s /bin/bash admin

RUN mkdir /app
RUN chown -R admin /app
USER admin

COPY ./dashboard/ ./app

WORKDIR /app

ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]