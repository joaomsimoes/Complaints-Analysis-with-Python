FROM python:3.7
WORKDIR .
COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt
ENV PORT=
COPY . ./
CMD streamlit run main.py --server.port=${PORT}  --browser.serverAddress="0.0.0.0"