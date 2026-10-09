FROM python:3.11-slim

WORKDIR /app 

COPY requirements.txt .    

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["streamlit", "run", "streamlit_app.py", "--server.address=0.0.0.0", "--server.port=8080"]


# FROM       → Base image
# WORKDIR    → Working directory
# COPY       → Copy files
# RUN        → Install dependencies
# EXPOSE     → Application port
# CMD        → Start application