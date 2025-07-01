# APOCALIPSSI - Analyse de Documents PDF

Une application Streamlit pour analyser et résumer des documents PDF avec l'aide de l'IA Hugging Face, incluant une gestion complète des sessions et des logs.

## 🚀 Fonctionnalités

### Analyse de Documents
- **Upload multiple** : Téléchargez plusieurs fichiers PDF simultanément
- **Extraction de texte** : Extraction automatique du contenu des PDF
- **Résumé automatique** : Génération de résumés avec l'IA Hugging Face
- **Chat interactif** : Posez des questions sur vos documents

### Gestion des Sessions
- **Sauvegarde automatique** : Les données sont automatiquement sauvegardées dans MongoDB
- **Reprise de session** : Reprenez votre travail là où vous l'avez laissé
- **Gestion des sessions** : Sauvegarde manuelle, effacement, et restauration

### Système de Logs
- **Logs d'activité** : Toutes les actions sont enregistrées dans la base de données
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

#### `activity_logs`
Enregistre toutes les activités utilisateur :
```json
{
  "timestamp": "2024-01-01T12:00:00Z",
  "activity_type": "file_uploaded",
  "user_id": "default",
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

## 📝 Types de Logs

L'application enregistre automatiquement les activités suivantes :

- `file_uploaded` : Upload d'un nouveau fichier
- `summaries_generated` : Génération de résumés
- `question_asked` : Questions posées à l'IA
- `session_restored` : Restauration d'une session
- `manual_save` : Sauvegarde manuelle
- `session_cleared` : Effacement de session
- `error_occurred` : Erreurs survenues

## 🎯 Utilisation

1. **Upload de documents** : Glissez-déposez vos PDF dans l'interface
2. **Analyse automatique** : Les documents sont analysés et les métadonnées affichées
3. **Génération de résumés** : Cliquez sur "Résumer les documents"
4. **Chat interactif** : Posez des questions dans la zone de chat
5. **Gestion des logs** : Utilisez la sidebar pour consulter les logs et gérer votre session

## 🔍 Fonctionnalités Avancées

### Sidebar de Gestion
- **Affichage des logs** : Consultez l'historique des activités
- **Informations de session** : ID de session et nombre de fichiers
- **Sauvegarde manuelle** : Forcez la sauvegarde de votre session
- **Effacement de session** : Réinitialisez complètement votre session

### Reprise Automatique
- Les données sont automatiquement sauvegardées à chaque action
- La session est restaurée au redémarrage de l'application
- Conservation de l'historique des conversations

## 🐛 Dépannage

### Problèmes de Connexion MongoDB
- Vérifiez votre chaîne de connexion dans `.streamlit/secrets.toml`
- Assurez-vous que votre cluster MongoDB Atlas est accessible
- Vérifiez les permissions de votre utilisateur MongoDB

### Problèmes d'API Hugging Face
- Vérifiez votre clé API dans `.streamlit/secrets.toml`
- Les modèles peuvent prendre du temps à se charger (503)
- L'application gère automatiquement les timeouts

## 📈 Améliorations Futures

- [ ] Interface d'administration pour les logs
- [ ] Export des données de session
- [ ] Support d'autres formats de documents
- [ ] Analyse de sentiment des documents
- [ ] Partage de sessions entre utilisateurs

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer des améliorations
- Soumettre des pull requests

## 📄 Licence

Ce projet est sous licence MIT.
