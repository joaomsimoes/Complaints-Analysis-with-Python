FROM python:3.7
EXPOSE 8501
WORKDIR .
COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD streamlit run --server.port 8501 --server.enableCORS false main.py