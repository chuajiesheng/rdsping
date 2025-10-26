FROM python:slim

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Install dependencies as root, then switch to non-root user
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip check

# Copy application files
COPY app.py .

# Change ownership to non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

EXPOSE 5000

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/reachability/app')"

CMD ["python", "app.py"]
