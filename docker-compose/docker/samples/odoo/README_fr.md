# Odoo avec docker-compose

Le fichier .env contient les variables d'environnement qui seront récupéré par docker-compose.yml
La commande docker-compose config permet de voir ce remplacement

```bash
sudo docker-compose config
```

Dans le cas du projet Odoo, le fichier de configuration **odoo.conf** qui sera monté à l'intérieur du container, doit être configuré avec les même variables que le fichier **.env** . Pour ce faire, nous avons crée un script en python **generate.py** qui lit le fichier .env et génère odoo.conf

Les modules sont placés dans le dossier modules sous forme de dépôt git.
```bash
sudo su dk
cd /opt/dk/projectName/modules/
git clone https://github.com/avenirbiz/absoins absoins
# adapt the .env
# Don't forget to adapt the addons path with volume in mounted directory
vim /opt/dk/projectName/.env
python3 generate.py
sudo systemctl restart dk@projectName
```
