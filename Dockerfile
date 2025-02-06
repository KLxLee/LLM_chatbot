# Stage 1: Build Stage
# Use an official Python runtime as a parent image
FROM python:3.12-slim AS build

# Set the working directory in the container
WORKDIR /app

# Copy only the necessary files for dependency installation
COPY pyproject.toml poetry.lock ./

# Install Poetry and project dependencies
RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction


# -------------------------------------------------------
# Stage 2: Final Stage (Runtime Image)
# Use a lightweight Python runtime for the final image
FROM python:3.12-slim AS final

# Set the working directory in the final image
WORKDIR /app

# Copy the installed dependencies from the build stage
COPY --from=build /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

# Copy the application code
COPY . .

EXPOSE 8000

# Specify the command to run the application
CMD ["python", "app/main.py"]
