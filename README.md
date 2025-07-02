# APOCALIPSSI - Analyse de Documents PDF

Une application Streamlit pour analyser et résumer des documents PDF avec l'aide de l'IA Hugging Face, incluant un système d'authentification complet et une gestion des sessions par utilisateur.

## 🚀 Fonctionnalités

### 🔐 Authentification
- **Inscription** : Création de compte avec nom d'utilisateur, email et mot de passe
- **Connexion** : Authentification sécurisée avec hashage des mots de passe
- **Déconnexion** : Gestion propre des sessions utilisateur
- **Sécurité** : Mots de passe hashés avec salt, validation des données

### 📄 Analyse de Documents
- **Upload multiple** : Téléchargez plusieurs fichiers PDF simultanément
- **Extraction de texte** : Extraction automatique du contenu des PDF
- **Résumé automatique** : Génération de résumés avec l'IA Hugging Face
- **Chat interactif** : Posez des questions sur vos documents

### 💾 Gestion des Sessions
- **Sauvegarde automatique** : Les données sont automatiquement sauvegardées dans MongoDB
- **Reprise de session** : Reprenez votre travail là où vous l'avez laissé
- **Sessions par utilisateur** : Chaque utilisateur a ses propres données
- **Gestion des sessions** : Sauvegarde manuelle, effacement, et restauration

### 📊 Système de Logs
- **Logs d'activité** : Toutes les actions sont enregistrées dans la base de données
- **Logs par utilisateur** : Chaque utilisateur voit ses propres logs
- **Historique complet** : Consultez l'historique des activités
- **Suivi des erreurs** : Logs automatiques des erreurs pour le débogage

## 🛠️ Installation

1. **Cloner le repository**
```bash
git clone <repository-url>
cd appocalIpssi
```

2. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

3. **Configuration des secrets**
Créez un fichier `.streamlit/secrets.toml` avec vos clés API :
```toml
[huggingface]
api_key = "votre_clé_api_huggingface"

[mongodb]
connection_string = "mongodb+srv://username:password@cluster.mongodb.net/"
```

4. **Lancer l'application**
```bash
streamlit run main.py
```

## 📊 Structure de la Base de Données

### Collections MongoDB

#### `users`
Stocke les informations des utilisateurs :
```json
{
  "_id": "ObjectId",
  "username": "nom_utilisateur",
  "email": "email@example.com",
  "password": "salt$hash",
  "created_at": "2024-01-01T12:00:00Z",
  "last_login": "2024-01-01T12:00:00Z",
  "is_active": true
}
```

#### `activity_logs`
Enregistre toutes les activités utilisateur :
```json
{
  "timestamp": "2024-01-01T12:00:00Z",
  "activity_type": "file_uploaded",
  "user_id": "user_id",
  "details": {
    "filename": "document.pdf",
    "pages": 10,
    "words": 5000,
    "session_id": "uuid-session"
  }
}
```

#### `sessions`
Stocke les données de session pour la reprise :
```json
{
  "session_id": "uuid-session",
  "user_id": "user_id",
  "data": {
    "file_texts": {...},
    "summaries": [...],
    "current_summaries": "...",
    "messages": [...]
  },
  "last_updated": "2024-01-01T12:00:00Z"
}
```

## 🔧 Configuration

Le fichier `config.py` centralise tous les paramètres de l'application :

- **MongoDB** : Nom de la base de données et collections
- **Logging** : Limites et paramètres des logs
- **Session** : Timeout et gestion des sessions
- **API** : Limites de texte et questions
- **Authentification** : Longueur minimale des mots de passe
- **Interface** : Titres et labels

## 🔐 Types de Logs

L'application enregistre automatiquement les activités suivantes :

- `user_registered` : Nouvelle inscription d'utilisateur
- `user_login` : Connexion d'utilisateur
- `user_logout` : Déconnexion d'utilisateur
- `file_uploaded` : Upload d'un nouveau fichier
- `summaries_generated` : Génération de résumés
- `question_asked` : Questions posées à l'IA
- `session_restored` : Restauration d'une session
- `manual_save` : Sauvegarde manuelle
- `session_cleared` : Effacement de session
- `error_occurred` : Erreurs survenues

## 🎯 Utilisation

### 🔐 Authentification
1. **Première visite** : Créez un compte ou connectez-vous
2. **Inscription** : Remplissez le formulaire avec vos informations
3. **Connexion** : Utilisez vos identifiants pour accéder à l'application
4. **Déconnexion** : Cliquez sur le bouton "🚪 Déconnexion"

### 📄 Analyse de Documents
1. **Upload de documents** : Glissez-déposez vos PDF dans l'interface
2. **Analyse automatique** : Les documents sont analysés et les métadonnées affichées
3. **Génération de résumés** : Cliquez sur "Résumer les documents"
4. **Chat interactif** : Posez des questions dans la zone de chat
5. **Gestion des logs** : Utilisez la sidebar pour consulter vos logs et gérer votre session

## 🔍 Fonctionnalités Avancées

### Sidebar de Gestion
- **Affichage des logs** : Consultez l'historique de vos activités
- **Informations de session** : ID de session et nombre de fichiers
- **Sauvegarde manuelle** : Forcez la sauvegarde de votre session
- **Effacement de session** : Réinitialisez complètement votre session

### Reprise Automatique
- Les données sont automatiquement sauvegardées à chaque action
- La session est restaurée au redémarrage de l'application
- Conservation de l'historique des conversations
- **Séparation par utilisateur** : Chaque utilisateur a ses propres données

### Sécurité
- **Hashage des mots de passe** : Utilisation de SHA-256 avec salt
- **Validation des données** : Vérification des entrées utilisateur
- **Gestion des sessions** : Sessions sécurisées par utilisateur
- **Logs d'audit** : Traçabilité complète des actions

## 🐛 Dépannage

### Problèmes d'Authentification
- Vérifiez que votre nom d'utilisateur et mot de passe sont corrects
- Assurez-vous que votre compte n'a pas été désactivé
- Les mots de passe doivent contenir au moins 6 caractères

### Problèmes de Connexion MongoDB
- Vérifiez votre chaîne de connexion dans `.streamlit/secrets.toml`
- Assurez-vous que votre cluster MongoDB Atlas est accessible
- Vérifiez les permissions de votre utilisateur MongoDB

### Problèmes d'API Hugging Face
- Vérifiez votre clé API dans `.streamlit/secrets.toml`
- Les modèles peuvent prendre du temps à se charger (503)
- L'application gère automatiquement les timeouts

## 📈 Améliorations Futures

- [ ] Interface d'administration pour les utilisateurs
- [ ] Récupération de mot de passe par email
- [ ] Authentification à deux facteurs
- [ ] Export des données de session
- [ ] Support d'autres formats de documents
- [ ] Analyse de sentiment des documents
- [ ] Partage de sessions entre utilisateurs
- [ ] API REST pour intégration externe

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer des améliorations
- Soumettre des pull requests

## 📄 Licence

Ce projet est sous licence MIT.
