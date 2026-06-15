# Use an official lightweight Python image as the base
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements first — Docker caches this layer so rebuilds are faster
COPY requirements.txt .

# Install all Python dependencies
RUN pip install -r requirements.txt

# Copy the rest of your project files into the container
COPY . .

# Tell Docker which port Streamlit runs on
EXPOSE 8501

# Command to run when the container starts
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]