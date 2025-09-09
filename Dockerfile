# Étend l'image officielle d'Airflow
FROM apache/airflow:2.9.1

# Passe en utilisateur root pour installer des paquets
USER root

# Installer uniquement Chromium et son driver
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Reviens à l'utilisateur airflow
USER airflow
	
# Copie requirements.txt dans le conteneur
COPY requirements.txt /requirements.txt

# Installe les dépendances Python
RUN pip install --no-cache-dir -r /requirements.txt


