# Use an official Python runtime as a parent image
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /app

# Install uv
RUN pip install uv

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the project files into the container
COPY . .

# Install dependencies using uv
RUN uv sync

ENV PATH="/app/.venv/bin:$PATH"
ENV UV_NO_DEV=1

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the application
CMD ["uvicorn", "src.magrathea.main:app", "--host", "0.0.0.0", "--port", "8000"]
