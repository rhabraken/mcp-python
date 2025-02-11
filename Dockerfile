FROM python:3.13

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy application files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Add wait-for-it script
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

# Start the app:
# - Wait for the database
# - Run create_tables.py first, then populate_db.py
CMD /wait-for-it.sh db:5432 -- python app/create_tables.py && python app/populate_db.py
