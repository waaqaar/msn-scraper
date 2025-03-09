FROM mcr.microsoft.com/playwright/python:v1.50.0-noble

# Set the working directory
WORKDIR /src

# Install dependencies
COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the script into the container
COPY src/scraper.py .

# Run the script
CMD ["python", "scraper.py"]
