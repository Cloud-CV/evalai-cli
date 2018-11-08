# Use Python 3.6 on Alpine Linux
FROM 3.6-alpine

# Copy source code
COPY . /cli

# Change working directory
WORKDIR /cli

# Install dependencies
RUN pip install -r requirements.txt

# Set Entrypoint as main.py
ENTRYPOINT ["python", "./evalai/main.py"]
