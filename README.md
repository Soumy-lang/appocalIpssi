### Installation

```bash
python -m pip install --upgrade pip setuptools wheel
python -m pip install --only-binary :all: scikit-learn
```

### Pré requis : 
- Installer Python 3 : [ici](https://www.python.org/downloads/)

### Clé API :
Renommer le fichier .streamlit/secrets.example.toml (ou similaire) en .streamlit/secrets.toml
Remplacer la valeur de la clé API par votre propre clé.

### Pour lancer l'app : 
- Créer un environnement virtuel python : ``` python -m venv venv ```
- Activer l'env : Mac ``` source venv/bin/activate ``` Win ``` venv\Scripts\activate ```
- Installer les dependances : ``` pip install -r requirements.txt ```
- lancer l'app : ``` streamlit run main.py ```
