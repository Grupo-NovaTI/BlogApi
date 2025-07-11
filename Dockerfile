# Stage 1: Builder
# This stage installs all the Python dependencies.
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies if any are needed for your packages
# RUN apt-get update && apt-get install -y --no-install-recommends build-essential

# Copy only the requirements file to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip wheel --no-cache-dir --wheel-dir /app/wheels -r requirements.txt


# Stage 2: Runtime
# This stage creates the final, smaller image.
FROM python:3.11-slim

WORKDIR /app

# Create a non-root user and group
RUN addgroup --system app && adduser --system --group app

# Copy installed dependencies from the builder stage
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

# Install the dependencies from the local wheels
RUN pip install --no-cache-dir /wheels/*

# Copy the application code
COPY ./app ./app

# Change ownership of the app directory to the non-root user
RUN chown -R app:app /app

# Switch to the non-root user
USER app

EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000"]