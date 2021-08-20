FROM python:3.7
WORKDIR .
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
ENV PORT=
COPY . ./
CMD streamlit run main.py --server.port=${PORT}  --browser.serverAddress="0.0.0.0"