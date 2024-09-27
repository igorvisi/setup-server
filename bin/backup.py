#!/usr/bin/env python3
import os
import subprocess
from datetime import datetime

# Variables générales
BASE_DIR = "/opt/dk"
LOG_FILE = "/var/log/restic-backup.log"
DEFAULT_KEEP_DAYS = 30  # Nombre de jours par défaut pour conserver les sauvegardes

# Informations de connexion en dur
RESTIC_PASSWORD = "pwd"  # Mot de passe Restic pour le chiffrement

# Liste des dépôts de sauvegarde
REPOSITORIES = [
    {
        "name": "StorageBox",
        "type": "sftp",
        "enabled": False,
        "user": "storagebox_user",
        "password": "storagebox_password",
        "provider": "storagebox.your-provider.com",
        "path": "/backups/{folder}",
        "keep_days": 15  # Personnalisation du nombre de jours
    },
    {
        "name": "ResticServer",
        "type": "rest",
        "enabled": True,
        "user": "visi",
        "password": "visi",
        "server_ip": "localhost:8000",
        "path": "/{folder}",
        "keep_days": 45  # Différent du défaut
    },
    {
        "name": "FTPS",
        "type": "ftps",
        "enabled": False,  # Désactivé si non utilisé
        "user": "",
        "password": "",
        "provider": "ftps.your-provider.com",
        "path": "/backups/{folder}",
        "keep_days": 30
    },
    {
        "name": "S3",
        "type": "s3",
        "enabled": False,  # Désactivé si non utilisé
        "bucket": "your-s3-bucket",
        "prefix": "backups/{folder}",
        "region": "us-west-2",
        "access_key": "YOUR_AWS_ACCESS_KEY_ID",
        "secret_key": "YOUR_AWS_SECRET_ACCESS_KEY",
        "endpoint": "",  # Laisser vide pour AWS S3, spécifier pour S3-like
        "keep_days": 60
    },
    {
        "name": "GCS",
        "type": "gcs",
        "enabled": False,  # Désactivé si non utilisé
        "bucket": "your-gcs-bucket",
        "prefix": "backups/{folder}",
        "credentials_file": "/path/to/your/credentials.json",
        "keep_days": 30
    },
    {
        "name": "AzureBlob",
        "type": "azure",
        "enabled": False,  # Désactivé si non utilisé
        "container": "your-azure-container",
        "prefix": "backups/{folder}",
        "account_name": "your-azure-account-name",
        "account_key": "your-azure-account-key",
        "keep_days": 30
    }
]

# Fonction de logging
def log_message(message):
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_FILE, 'a') as log:
        log.write(f"[{date}] {message}\n")
    print(message)  # Affiche également les messages sur la CLI

# Fonction de gestion des erreurs
def handle_error(message):
    log_message(f"ERROR: {message}")
    exit(1)

# Fonction pour exécuter les commandes Restic
def run_restic_command(command):
    log_message(f"Executing: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        handle_error(result.stderr)
    log_message(result.stdout)

# Fonction pour initialiser le dépôt Restic si non existant
def init_restic_repository(repository_url, repo_name):
    log_message(f"Checking if repository '{repo_name}' needs initialization...")
    # Essayer d'accéder aux snapshots pour voir si le dépôt existe
    command = f"restic snapshots -r {repository_url}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if "Fatal: unable to open config file" in result.stderr or "Fatal: repository does not exist" in result.stderr:
        # Le dépôt n'existe pas encore, il faut l'initialiser
        log_message(f"Initializing new restic repository '{repo_name}' at {repository_url}")
        init_command = f"restic init -r {repository_url}"
        run_restic_command(init_command)
    elif "Fatal: wrong password" in result.stderr:
        handle_error(f"Wrong password for repository '{repo_name}' at {repository_url}")
    else:
        log_message(f"Repository '{repo_name}' already initialized.")

# Fonction pour configurer les variables d'environnement spécifiques aux backends
def set_backend_env(repo):
    if repo["type"] == "s3":
        os.environ['AWS_ACCESS_KEY_ID'] = repo["access_key"]
        os.environ['AWS_SECRET_ACCESS_KEY'] = repo["secret_key"]
        if repo["endpoint"]:
            os.environ['RESTIC_S3_ENDPOINT'] = repo["endpoint"]
        os.environ['RESTIC_S3_REGION'] = repo["region"]
    elif repo["type"] == "gcs":
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = repo["credentials_file"]
    elif repo["type"] == "azure":
        os.environ['AZURE_STORAGE_ACCOUNT'] = repo["account_name"]
        os.environ['AZURE_STORAGE_KEY'] = repo["account_key"]
    # Ajouter d'autres backends si nécessaire

# Fonction de sauvegarde Restic pour chaque dossier
def backup_folder(folder, repository_url, repo_name, repo_type, repo_config):
    log_message(f"Starting backup of '{folder}' to repository '{repo_name}' ({repo_type})...")

    # Définir les variables d'environnement nécessaires pour Restic
    os.environ['RESTIC_REPOSITORY'] = repository_url
    os.environ['RESTIC_PASSWORD'] = RESTIC_PASSWORD  # Mot de passe en dur

    # Configurer les variables d'environnement spécifiques au backend
    set_backend_env(repo_config)

    # Initialiser le dépôt si nécessaire
    init_restic_repository(repository_url, repo_name)

    # Exécuter la sauvegarde
    backup_command = f"restic backup {folder} --verbose"
    run_restic_command(backup_command)
    log_message(f"Backup of '{folder}' to repository '{repo_name}' completed successfully.")

    # Exécuter les statistiques
    stats_command = "restic stats"
    run_restic_command(stats_command)

    # Exécuter la commande forget avec rétention
    keep_days = repo_config.get("keep_days", DEFAULT_KEEP_DAYS)
    forget_command = f"restic forget --keep-daily {keep_days} --prune -r {repository_url}"
    run_restic_command(forget_command)

# Sauvegarde pour chaque sous-dossier
def backup_all_folders():
    for folder in os.listdir(BASE_DIR):
        folder_path = os.path.join(BASE_DIR, folder)

        # Vérifier si c'est un répertoire
        if os.path.isdir(folder_path):
            log_message(f"Processing folder: {folder_path}")
            # Boucler sur chaque dépôt
            for repo in REPOSITORIES:
                if not repo.get("enabled", False):
                    continue  # Passer les dépôts désactivés

                repo_type = repo["type"]
                repo_name = repo["name"]

                try:
                    if repo_type == "sftp":
                        # Vérifier les informations nécessaires
                        if not (repo["user"] and repo["password"] and repo["provider"]):
                            log_message(f"Skipping SFTP repository '{repo_name}' due to missing configuration.")
                            continue
                        repository_url = f"sftp://{repo['user']}:{repo['password']}@{repo['provider']}{repo['path'].format(folder=folder)}"
                        backup_folder(folder_path, repository_url, repo_name, repo_type, repo)

                    elif repo_type == "rest":
                        # Vérifier les informations nécessaires
                        if not (repo["user"] and repo["password"] and repo["server_ip"]):
                            log_message(f"Skipping REST repository '{repo_name}' due to missing configuration.")
                            continue
                        repository_url = f"rest:http://{repo['user']}:{repo['password']}@{repo['server_ip']}{repo['path'].format(folder=folder)}"
                        backup_folder(folder_path, repository_url, repo_name, repo_type, repo)

                    elif repo_type == "ftps":
                        # Vérifier les informations nécessaires
                        if not (repo["user"] and repo["password"] and repo["provider"]):
                            log_message(f"Skipping FTPS repository '{repo_name}' due to missing configuration.")
                            continue
                        repository_url = f"ftps://{repo['user']}:{repo['password']}@{repo['provider']}{repo['path'].format(folder=folder)}"
                        backup_folder(folder_path, repository_url, repo_name, repo_type, repo)

                    elif repo_type == "s3":
                        # Vérifier les informations nécessaires
                        if not (repo["bucket"] and repo["prefix"] and repo["access_key"] and repo["secret_key"] and repo["region"]):
                            log_message(f"Skipping S3 repository '{repo_name}' due to missing configuration.")
                            continue
                        repository_url = f"s3://{repo['bucket']}/{repo['prefix'].format(folder=folder)}"
                        backup_folder(folder_path, repository_url, repo_name, repo_type, repo)

                    elif repo_type == "gcs":
                        # Vérifier les informations nécessaires
                        if not (repo["bucket"] and repo["prefix"] and repo["credentials_file"]):
                            log_message(f"Skipping GCS repository '{repo_name}' due to missing configuration.")
                            continue
                        repository_url = f"gs://{repo['bucket']}/{repo['prefix'].format(folder=folder)}"
                        backup_folder(folder_path, repository_url, repo_name, repo_type, repo)

                    elif repo_type == "azure":
                        # Vérifier les informations nécessaires
                        if not (repo["container"] and repo["prefix"] and repo["account_name"] and repo["account_key"]):
                            log_message(f"Skipping Azure Blob repository '{repo_name}' due to missing configuration.")
                            continue
                        repository_url = f"azure:{repo['container']}/{repo['prefix'].format(folder=folder)}"
                        backup_folder(folder_path, repository_url, repo_name, repo_type, repo)

                    else:
                        log_message(f"Unknown repository type '{repo_type}' for repository '{repo_name}'. Skipping.")

                except Exception as e:
                    handle_error(f"Exception occurred while processing repository '{repo_name}': {str(e)}")

# Lancer la sauvegarde
if __name__ == "__main__":
    log_message("Backup process started.")
    backup_all_folders()
    log_message("Backup process completed.")

