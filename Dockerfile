FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy project and install as a package so console script is available
COPY . .
RUN pip install --no-cache-dir .

ENTRYPOINT ["balancefetcher"]
