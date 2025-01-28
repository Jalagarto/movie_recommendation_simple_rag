# Use an official Python runtime as the base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /src/app

# Copy the requirements file into the container
COPY pyproject.toml poetry.lock ./
COPY .env /src

# Install Poetry and project dependencies
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction --no-ansi

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
# CMD ["streamlit", "run", "src/app/serve.py"]
CMD ["streamlit", "run", "src/app/serve.py", "--server.port", "8000"]