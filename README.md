# 🖥️ CoreAnalystics

Application de diagnostic PC en Python + CustomTkinter.
Dépôt privé — accès par token GitHub.

## ⚡ Installation

```bash
pip install -r requirements.txt
```

## 🚀 Lancement

```bash
python main.py
```

## 📁 Structure

```
CoreAnalystics/
├── main.py                  ← Point d'entrée
├── requirements.txt         ← Dépendances
├── ui/
│   ├── splash.py            ← Écran de chargement
│   └── dashboard.py         ← Écran d'accueil
└── modules/
    ├── updater.py            ← Auto-update GitHub (privé)
    ├── cpu_ram.py            ← Module CPU/RAM (à venir)
    ├── disk.py               ← Module Disque (à venir)
    ├── network.py            ← Module Réseau (à venir)
    └── logs.py               ← Module Logs (à venir)
```

---

## 🔑 Token GitHub — Comment en créer un

Le dépôt étant **privé**, l'auto-updater a besoin d'un token
pour accéder à l'API GitHub. Voici comment en créer un :

1. Va sur **github.com** → clique sur ta photo en haut à droite
2. **Settings** → tout en bas : **Developer settings**
3. **Personal access tokens** → **Tokens (classic)**
4. Clique **"Generate new token (classic)"**
5. Remplis :
   - **Note** : `CoreAnalystics Updater`
   - **Expiration** : `No expiration` (ou la durée que tu veux)
   - **Scopes** : coche uniquement `repo` ✅
6. Clique **"Generate token"**
7. **Copie le token** (il ne sera affiché qu'une seule fois !)
8. Colle-le dans `modules/updater.py` :

```python
GITHUB_TOKEN = "ghp_xxxxxxxxxxxxxxxxxxxx"  # ← ton token ici
```

> ⚠️ Ne commit jamais le fichier avec le vrai token dedans !
> Ajoute `modules/updater.py` dans ton `.gitignore` ou utilise
> un fichier `.env` séparé (voir section suivante).

---

## 🛡️ Bonne pratique — stocker le token dans un .env

Pour éviter d'exposer ton token dans le code :

**1. Crée un fichier `.env`** à la racine du projet :
```
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
```

**2. Ajoute `.env` dans `.gitignore`** :
```
.env
```

**3. Installe python-dotenv** :
```bash
pip install python-dotenv
```

**4. Dans `updater.py`**, remplace la ligne du token par :
```python
from dotenv import load_dotenv
import os
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
```

---

## 🔄 Publier une mise à jour

1. Zippe le projet → `CoreAnalystics_v0.2.0.zip`
2. Sur GitHub → **Releases** → **Create a new release**
3. Tag : `v0.2.0` · attache le `.zip` · publie
4. L'app détecte la nouvelle version au prochain démarrage ✓

