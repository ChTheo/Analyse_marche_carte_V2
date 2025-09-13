# Étend l'image officielle d'Airflow
FROM apache/airflow:2.9.1

# Passe en utilisateur root pour installer des paquets
USER root
RUN mkdir -p /opt/airflow/backups && chmod -R 777 /opt/airflow/backups
# Installer Chromium version fixe et unzip pour webdriver-manager
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    --no-install-recommends && \
    wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable=140.0.7339.127-1 --no-install-recommends && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Reviens à l'utilisateur airflow
USER airflow

# Copie requirements.txt dans le conteneur
COPY requirements.txt /requirements.txt

# Installe les dépendances Python
RUN pip install --no-cache-dir -r /requirements.txt
