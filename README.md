# 🎃 Halloween Quiz 2025 👻

Application web de quiz Halloween avec système de QR codes et leaderboard pour votre soirée d'Halloween !

## 📋 Description

Cette application Flask permet de créer un jeu de piste Halloween avec :
- Des QR codes à placer dans votre appartement
- Des questions sur le thème d'Halloween
- Un système de points (1 point par bonne réponse)
- Un leaderboard en temps réel
- Interface responsive et thème Halloween

## 🚀 Démarrage rapide

### Prérequis
- Docker et Docker Compose installés sur votre Raspberry Pi
- Python 3.11+ (pour le développement local)

### Installation sur Raspberry Pi

1. **Cloner le repository**
```bash
git clone https://github.com/SephyrothC/Halloween_2025.git
cd Halloween_2025
```

2. **Copier le fichier d'exemple des questions**
```bash
cp data/questions_example.json data/questions.json
```

3. **Personnaliser les questions** (optionnel)
Éditez `data/questions.json` pour ajouter vos propres questions.

4. **Lancer avec Docker Compose**
```bash
docker-compose up -d
```

L'application sera accessible sur `http://<IP_DE_VOTRE_RASPPI>:5000`

5. **Vérifier que l'application fonctionne**
```bash
docker-compose logs -f
```

## 🔧 Configuration

### Structure des questions

Le fichier `data/questions.json` contient toutes les questions au format suivant :

```json
{
  "1": {
    "question": "Votre question ici ?",
    "choices": [
      "Choix 1",
      "Choix 2",
      "Choix 3",
      "Choix 4"
    ],
    "correct": "La bonne réponse"
  }
}
```

### Ajouter des questions

1. Ouvrez `data/questions.json`
2. Ajoutez une nouvelle entrée avec un ID unique
3. Redémarrez le conteneur : `docker-compose restart`

## 📱 Génération des QR Codes

### Méthode 1 : En ligne
Utilisez un générateur de QR code en ligne comme :
- https://www.qr-code-generator.com/
- https://www.qrcode-monkey.com/

Pour chaque question, générez un QR code pointant vers :
```
http://<IP_DE_VOTRE_RASPPI>:5000/quiz/1
http://<IP_DE_VOTRE_RASPPI>:5000/quiz/2
...
```

### Méthode 2 : Script Python (recommandé)

Créez un fichier `generate_qr.py` :

```python
import qrcode
import os

# Remplacez par l'IP de votre Raspberry Pi
RASPBERRY_PI_IP = "192.168.1.100"  # À MODIFIER
BASE_URL = f"http://{RASPBERRY_PI_IP}:5000/quiz/"

# Nombre de questions
NUM_QUESTIONS = 10

# Créer le dossier pour les QR codes
os.makedirs("qr_codes", exist_ok=True)

for i in range(1, NUM_QUESTIONS + 1):
    url = f"{BASE_URL}{i}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(f"qr_codes/question_{i}.png")
    print(f"QR Code généré pour la question {i}")

print(f"\n✅ {NUM_QUESTIONS} QR codes générés dans le dossier 'qr_codes/'")
```

Installez les dépendances et lancez :
```bash
pip install qrcode[pil]
python generate_qr.py
```

### Impression des QR codes

1. Imprimez les images générées dans `qr_codes/`
2. Découpez-les ou plastifiez-les
3. Cachez-les dans votre appartement !

## 🎮 Utilisation

### Pour les organisateurs

1. **Démarrer l'application** avant l'arrivée des invités
2. **Cacher les QR codes** dans l'appartement
3. **Consulter le leaderboard** sur un écran : `http://<IP_RASPPI>:5000/leaderboard`

### Pour les joueurs

1. Scanner un QR code avec leur smartphone
2. Entrer leur nom
3. Répondre à la question
4. Consulter le leaderboard pour voir leur classement

## 🛠️ Commandes utiles

### Docker

```bash
# Démarrer l'application
docker-compose up -d

# Arrêter l'application
docker-compose down

# Voir les logs
docker-compose logs -f

# Redémarrer après modification
docker-compose restart

# Reconstruire l'image
docker-compose up -d --build
```

### Développement local

```bash
# Installer les dépendances
pip install -r requirements.txt

# Lancer en mode développement
python app.py
```

L'application sera accessible sur `http://localhost:5000`

## 📊 Routes disponibles

- `/` - Page d'accueil
- `/quiz/<id>` - Page de question (ex: /quiz/1)
- `/leaderboard` - Classement des joueurs
- `/api/leaderboard` - API JSON du classement
- `/reset` - Réinitialiser la session (pour tester)

## 🔒 Sécurité et conseils

1. **Changez la clé secrète** dans `app.py` :
```python
app.secret_key = 'votre-cle-super-secrete-unique'
```

2. **Pour un réseau local uniquement** : Le serveur écoute sur `0.0.0.0:5000`

3. **Sauvegarde des scores** : Les scores sont dans `data/scores.json` (persisté via Docker volume)

## 🎨 Personnalisation

### Thème CSS
Modifiez `static/css/style.css` pour changer les couleurs et le style.

### Templates
Les templates HTML sont dans le dossier `templates/` :
- `base.html` - Template de base
- `index.html` - Page d'accueil
- `quiz.html` - Page de question
- `leaderboard.html` - Page du classement

## 🐛 Dépannage

### L'application ne démarre pas
```bash
# Vérifier les logs
docker-compose logs

# Vérifier que le port 5000 est libre
sudo netstat -tulpn | grep 5000
```

### Les données ne persistent pas
Vérifiez que le dossier `data/` existe et contient `questions.json` et `scores.json`

### Les QR codes ne fonctionnent pas
- Vérifiez l'IP de votre Raspberry Pi : `hostname -I`
- Assurez-vous que les appareils sont sur le même réseau WiFi
- Testez l'URL dans un navigateur avant de générer les QR codes

## 📝 Structure du projet

```
Halloween_2025/
├── app.py                      # Application Flask principale
├── requirements.txt            # Dépendances Python
├── Dockerfile                  # Configuration Docker
├── docker-compose.yml          # Configuration Docker Compose
├── README.md                   # Ce fichier
├── data/
│   ├── questions.json          # Questions du quiz (à créer)
│   ├── questions_example.json  # Exemple de questions
│   └── scores.json             # Scores des joueurs (auto-créé)
├── templates/
│   ├── base.html              # Template de base
│   ├── index.html             # Page d'accueil
│   ├── quiz.html              # Page de question
│   └── leaderboard.html       # Page du leaderboard
└── static/
    └── css/
        └── style.css          # Styles CSS
```

## 🎉 Améliorations futures

- [ ] Ajouter des catégories de questions
- [ ] Timer pour chaque question
- [ ] Bonus pour les réponses rapides
- [ ] Mode multijoueur en temps réel
- [ ] Interface d'administration
- [ ] Export des résultats en CSV
- [ ] Sons et effets spéciaux

## 📜 Licence

Ce projet est libre d'utilisation pour vos soirées Halloween ! 🎃

## 🤝 Contribution

N'hésitez pas à proposer des améliorations ou des questions supplémentaires !

---

**Joyeux Halloween ! 🎃👻🦇**
