# Analyseur de Documents PDF avec IA et MongoDB

Cette application Streamlit permet d'analyser des fichiers PDF, de générer des résumés avec l'IA et de stocker toutes les données dans MongoDB Atlas.

## Architecture

L'application utilise une architecture modulaire avec :
- `main.py` : Interface utilisateur Streamlit
- `database.py` : Gestionnaire de base de données MongoDB
- `.env` : Variables d'environnement (clés API et configuration)
- `env_example.txt` : Exemple de configuration

## Fonctionnalités

- 📄 Upload et analyse de fichiers PDF
- 🤖 Génération de résumés avec OpenAI GPT
- 💬 Chat interactif avec les documents
- 🗄️ Stockage persistant dans MongoDB Atlas
- 📊 Historique et statistiques des documents

## Configuration

### 1. Installation des dépendances

```bash
pip install -r requirements.txt
```

### 2. Configuration des variables d'environnement

1. Renommez `env_example.txt` en `.env`
2. Modifiez le fichier `.env` avec vos informations :

<<<<<<< HEAD
```env
# Configuration OpenAI
OPENAI_API_KEY=votre_clé_api_openai_ici

# Configuration MongoDB Atlas
MONGODB_CONNECTION_STRING=mongodb+srv://votre_utilisateur:votre_mot_de_passe@votre_cluster.mongodb.net/?retryWrites=true&w=majority

# Configuration de l'application
APP_NAME=Analyseur de Documents PDF
APP_VERSION=1.0.0
```

### 3. Configuration MongoDB Atlas

1. Créez un compte sur [MongoDB Atlas](https://www.mongodb.com/atlas)
2. Créez un nouveau cluster
3. Créez un utilisateur de base de données
4. Obtenez votre chaîne de connexion et ajoutez-la dans le fichier `.env`

### 4. Structure de la base de données

L'application crée automatiquement les collections suivantes :
- `documents` : Stockage des fichiers PDF traités
- `summaries` : Historique des résumés générés
- `conversations` : Historique des conversations avec l'IA

### 5. Gestionnaire de base de données

Le fichier `database.py` contient la classe `DatabaseManager` qui gère :
- Connexion automatique à MongoDB Atlas
- Opérations CRUD pour les documents, résumés et conversations
- Gestion des erreurs et reconnexion
- Méthodes utilitaires pour les requêtes courantes

## Lancement de l'application

### Développement local

```bash
# Installer les dépendances
pip install -r requirements.txt

# Configurer les variables d'environnement
cp env_example.txt .env
# Éditer le fichier .env avec vos clés API

# Lancer l'application
streamlit run main.py
```

### Variables d'environnement requises

| Variable | Description | Exemple |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Clé API OpenAI | `sk-...` |
| `MONGODB_CONNECTION_STRING` | Chaîne de connexion MongoDB Atlas | `mongodb+srv://...` |
| `APP_NAME` | Nom de l'application | `Analyseur de Documents PDF` |
| `APP_VERSION` | Version de l'application | `1.0.0` |

## Utilisation

1. **Upload de documents** : Glissez-déposez vos fichiers PDF
2. **Génération de résumés** : Cliquez sur "Résumer les documents"
3. **Chat interactif** : Posez des questions sur vos documents
4. **Historique** : Consultez les statistiques et l'historique dans la base de données

## Sécurité

- Les clés API sont stockées dans le fichier `.env` (non versionné)
- La connexion MongoDB utilise SSL par défaut
- Les données sensibles ne sont pas exposées dans le code
- Le fichier `.env` doit être ajouté au `.gitignore`

## Support

Pour toute question ou problème, consultez la documentation de :
- [Streamlit](https://docs.streamlit.io/)
- [MongoDB Atlas](https://docs.atlas.mongodb.com/)
- [OpenAI API](https://platform.openai.com/docs/)
=======
### Pour lancer l'app : 
- Créer un environnement virtuel python 
```bash
  python -m venv venv 
```

- Activer l'env 
```bash
Mac : source venv/bin/activate 
Windows : venv\Scripts\activate 
```

- Installer les dependances
```bash
 pip install -r requirements.txt 
 ```
 
- lancer l'app  
```bash
streamlit run main.py 
```
>>>>>>> 83b677f0b34e628928b2ed35efeada2f9a8408ee
