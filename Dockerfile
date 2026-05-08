FROM python:3.10-slim

WORKDIR /rag_app 

COPY . . 

RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

RUN pip install --timeout=1000 torch --index-url https://download.pytorch.org/whl/cpu

RUN pip install -r requirements.txt 

RUN pip list 

CMD ["python" , "src/main.py"]
