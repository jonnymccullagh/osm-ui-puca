# Base image with Python 3.13
FROM python:3.13-slim

# Set working directory inside the container
WORKDIR /app

# Copy the Python script and .env file into the container
COPY app/ /app/

# Install uv and your required Python libraries (fastmcp, httpx)
RUN pip install --no-cache-dir uv
RUN uv pip install -r requirements.txt

# Expose the port that will be used (can also be set via the .env file)
EXPOSE 8501

# Set the command to run the application
CMD ["sh", "-c", "streamlit run server.py"]
