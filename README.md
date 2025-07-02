# APOCALIPSSI - Analyse de Documents PDF

Une application Streamlit pour analyser et résumer des documents PDF avec l'aide de l'IA Hugging Face, incluant un système d'authentification complet et une gestion des sessions utilisateur.

## 🚀 Fonctionnalités

### 🔐 Système d'Authentification
- **Inscription sécurisée** : Création de compte avec validation des données
- **Connexion utilisateur** : Authentification avec email et mot de passe
- **Validation des mots de passe** : Exigences de sécurité (8+ caractères, majuscule, minuscule, chiffre)
- **Messages de succès** : Notifications visuelles avec animations
- **Redirection automatique** : Après inscription réussie, redirection vers la page de connexion
- **Déconnexion** : Bouton de déconnexion dans la sidebar

### Analyse de Documents
- **Upload multiple** : Téléchargez plusieurs fichiers PDF simultanément
- **Extraction de texte** : Extraction automatique du contenu des PDF
- **Résumé automatique** : Génération de résumés avec l'IA Hugging Face
- **Chat interactif** : Posez des questions sur vos documents

### Gestion des Sessions
- **Sauvegarde automatique** : Les données sont automatiquement sauvegardées dans MongoDB
- **Reprise de session** : Reprenez votre travail là où vous l'avez laissé
- **Gestion des sessions** : Sauvegarde manuelle, effacement, et restauration
- **Sessions par utilisateur** : Chaque utilisateur a ses propres sessions

### Système de Logs
- **Logs d'activité** : Toutes les actions sont enregistrées dans la base de données
- **Historique complet** : Consultez l'historique des activités par utilisateur
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
  "email": "utilisateur@email.com",
  "password": "hash_sha256_du_mot_de_passe",
  "full_name": "Nom Complet",
  "created_at": "2024-01-01T12:00:00Z",
  "last_login": "2024-01-01T12:00:00Z"
}
```

#### `activity_logs`
Enregistre toutes les activités utilisateur :
```json
{
  "timestamp": "2024-01-01T12:00:00Z",
  "activity_type": "file_uploaded",
  "user_id": "utilisateur@email.com",
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
- **Interface** : Titres et labels
- **Authentification** : Exigences des mots de passe

## 🔐 Sécurité

### Validation des Mots de Passe
- **Longueur minimale** : 8 caractères
- **Complexité requise** : Majuscule, minuscule, chiffre
- **Hachage sécurisé** : SHA-256 pour le stockage
- **Validation en temps réel** : Feedback immédiat sur la force du mot de passe

### Protection des Données
- **Mots de passe hachés** : Jamais stockés en clair
- **Validation des emails** : Format email vérifié
- **Sessions sécurisées** : ID de session unique par utilisateur
- **Logs utilisateur** : Traçabilité complète des actions

## 📝 Types de Logs

L'application enregistre automatiquement les activités suivantes :

- `user_registered` : Nouvelle inscription d'utilisateur
- `user_logged_in` : Connexion d'utilisateur
- `file_uploaded` : Upload d'un nouveau fichier
- `summaries_generated` : Génération de résumés
- `question_asked` : Questions posées à l'IA
- `session_restored` : Restauration d'une session
- `manual_save` : Sauvegarde manuelle
- `session_cleared` : Effacement de session
- `error_occurred` : Erreurs survenues

## 🎯 Utilisation

### Première Utilisation
1. **Accéder à l'application** : Ouvrez l'URL de l'application
2. **Créer un compte** : Cliquez sur l'onglet "Inscription"
3. **Remplir le formulaire** : Nom complet, email, mot de passe
4. **Validation automatique** : Le système vérifie les données
5. **Message de succès** : Confirmation avec animation
6. **Redirection automatique** : Vers la page de connexion

### Utilisation Quotidienne
1. **Se connecter** : Email et mot de passe
2. **Upload de documents** : Glissez-déposez vos PDF
3. **Analyse automatique** : Les documents sont analysés
4. **Génération de résumés** : Cliquez sur "Résumer les documents"
5. **Chat interactif** : Posez des questions dans la zone de chat
6. **Gestion des logs** : Utilisez la sidebar pour consulter les logs
7. **Se déconnecter** : Bouton dans la sidebar

## 🔍 Fonctionnalités Avancées

### Interface d'Authentification
- **Design moderne** : Interface utilisateur attrayante
- **Validation en temps réel** : Feedback immédiat
- **Messages d'erreur clairs** : Explications détaillées
- **Animations de succès** : Confettis et ballons
- **Redirection intelligente** : Navigation fluide

### Sidebar de Gestion
- **Informations utilisateur** : Nom affiché en haut
- **Affichage des logs** : Consultez l'historique des activités
- **Informations de session** : ID de session et nombre de fichiers
- **Sauvegarde manuelle** : Forcez la sauvegarde de votre session
- **Effacement de session** : Réinitialisez complètement votre session
- **Bouton de déconnexion** : Déconnexion sécurisée

### Reprise Automatique
- **Sessions par utilisateur** : Chaque utilisateur a ses propres données
- **Sauvegarde automatique** : Les données sont sauvegardées à chaque action
- **Restauration au redémarrage** : La session est restaurée automatiquement
- **Conservation de l'historique** : Conversations et analyses préservées

## 🐛 Dépannage

### Problèmes d'Inscription
- **Email déjà utilisé** : Utilisez un autre email
- **Mot de passe faible** : Respectez les exigences de sécurité
- **Validation échouée** : Vérifiez le format de l'email

### Problèmes de Connexion
- **Email incorrect** : Vérifiez l'orthographe
- **Mot de passe oublié** : Contactez l'administrateur
- **Compte inexistant** : Créez un nouveau compte

### Problèmes de Connexion MongoDB
- Vérifiez votre chaîne de connexion dans `.streamlit/secrets.toml`
- Assurez-vous que votre cluster MongoDB Atlas est accessible
- Vérifiez les permissions de votre utilisateur MongoDB

### Problèmes d'API Hugging Face
- Vérifiez votre clé API dans `.streamlit/secrets.toml`
- Les modèles peuvent prendre du temps à se charger (503)
- L'application gère automatiquement les timeouts

## 📈 Améliorations Futures

- [ ] Réinitialisation de mot de passe par email
- [ ] Authentification à deux facteurs
- [ ] Gestion des rôles utilisateur
- [ ] Interface d'administration pour les utilisateurs
- [ ] Export des données de session
- [ ] Support d'autres formats de documents
- [ ] Analyse de sentiment des documents
- [ ] Partage de sessions entre utilisateurs
- [ ] Notifications par email
- [ ] Historique des connexions

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer des améliorations
- Soumettre des pull requests

## 📄 Licence

Ce projet est sous licence MIT.
