FROM python:3.6-alpine

# Install gcc and a few other required libraries
RUN apk add build-base python3-dev libxml2-dev libxslt-dev zlib-dev

# Install dependencies from requirements.txt (on top to make use of layer caching)
COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt

# Copy source code
COPY . /cli

# Change working directory
WORKDIR /cli

# Install package locally
RUN pip install -e .

# Set Entrypoint as evalai
ENTRYPOINT ["evalai"]
