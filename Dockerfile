# Use Python 3.11 slim for a smaller image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the agent package
COPY aero_inspector/ ./aero_inspector/

# Expose port (Render sets PORT env var automatically)
EXPOSE 8080

# Launch the ADK web server — use shell form so $PORT is expanded
CMD adk web --port ${PORT:-8080} aero_inspector
