# --- Stage 1: The Builder ---
# This stage installs dependencies into a self-contained directory.
FROM python:3.9-slim AS builder

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first to leverage Docker's layer caching
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt


# --- Stage 2: The Final Image ---
# This stage builds the lean, final image for production.
FROM python:3.9-slim

WORKDIR /app

# Copy the installed packages from the 'builder' stage
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

# Copy your application code and templates folder
COPY app.py .
COPY templates/ templates/

# Tell Docker that the container listens on port 3333
EXPOSE 3333

# The command to run when the container starts
CMD ["python", "app.py"]
