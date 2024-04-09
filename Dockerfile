FROM python:3.11-slim

COPY ./requirements.txt ./

RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN useradd -m -s /bin/bash admin

RUN mkdir /app
RUN chown -R admin /app
USER admin

COPY ./dashboard/main.py ./app
COPY ./dashboard/helper.py ./app
COPY ./dashboard/overall.py ./app
COPY ./dashboard/category.py ./app

WORKDIR /app

ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]