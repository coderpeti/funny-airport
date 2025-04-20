# Python 3 base image
FROM python:3.11-slim

# Install basic system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget curl unzip gnupg ca-certificates \
    fonts-liberation libappindicator3-1 libasound2 \
    libatk-bridge2.0-0 libatk1.0-0 libcups2 libdbus-1-3 \
    libgdk-pixbuf2.0-0 libnspr4 libnss3 libx11-xcb1 \
    libxcomposite1 libxdamage1 libxrandr2 xdg-utils \
    libu2f-udev libvulkan1 && \
    rm -rf /var/lib/apt/lists/*

# Install the latest version of Google Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# Copy and run ChromeDriver installer script
COPY get_chromedriver.sh /tmp/get_chromedriver.sh
RUN chmod +x /tmp/get_chromedriver.sh && /tmp/get_chromedriver.sh

# Set working directory
WORKDIR /usr/src/app

# Copy application files
COPY . /usr/src/app

# Install Python packages
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Start Django server
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
