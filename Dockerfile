FROM python:3.8-slim
WORKDIR .
COPY requirements.txt .
RUN pip3 install -r requirements.txt
ENV PORT=
COPY . ./
CMD streamlit run main.py --server.port=${PORT}  --browser.serverAddress="0.0.0.0"