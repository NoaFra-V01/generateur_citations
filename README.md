# 🏰 Inspire Me — Générateur de Répliques Kaamelott

> *"C'est pas faux."* — Perceval

Un script Python qui affiche des répliques cultes de la série **Kaamelott** directement dans votre terminal ! ⚔️

---

## ✨ Fonctionnalités

| Fonctionnalité | Description |
|----------------|-------------|
| 🌐 **API Kaamelott** | Récupère des répliques aléatoires parmi **765 citations** |
| 📚 **Mode hors-ligne** | Fallback intelligent avec citations locales |
| 🎨 **Affichage stylé** | Cadre Unicode élégant dans le terminal |
| 💾 **Sauvegarde** | Possibilité d'enregistrer la citation dans un fichier |
| 🔒 **Sécurisé** | Protection contre les injections de chemin |
| 🐍 **Sans dépendance** | 100% bibliothèque standard Python |

---

## 🚀 Installation

### Prérequis

- Python 3.7 ou supérieur

### Téléchargement

```bash
# Cloner ou télécharger le fichier
curl -O inspire_me.py

# Ou simplement copier le fichier inspire_me.py dans votre dossier
```

Aucune installation de dépendances requise ! 🎉

---

## 📖 Utilisation

### Lancement basique

```bash
python3 inspire_me.py
```

### Exemple de sortie

```
🔍 Recherche d'une réplique culte...

╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║  C'est pas faux. — Perceval                                               ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝

Voulez-vous sauvegarder cette citation ? (o/n) : o
✓ Citation sauvegardée dans 'citation.txt'
```

### Options de sauvegarde

Quand le script vous demande si vous voulez sauvegarder, vous pouvez répondre :

| Réponse | Action |
|---------|--------|
| `o`, `oui`, `y`, `yes` | ✅ Sauvegarde dans `citation.txt` |
| Toute autre réponse | ❌ Pas de sauvegarde |

---

## 🔧 Comment ça marche

### Architecture

```
                    ┌─────────────────────┐
                    │   🌐 Internet       │
                    │  API Kaamelott      │
                    └──────────┬──────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────┐
│              inspire_me.py                       │
├──────────────────────────────────────────────────┤
│                                                  │
│   1. 🔍 Tente de récupérer une réplique en ligne │
│                     │                            │
│            ┌───────┴───────┐                     │
│            ▼               ▼                     │
│        Succès ?        Échec ?                   │
│            │               │                     │
│            ▼               ▼                     │
│    Réplique web    📚 Fallback local             │
│                                                  │
│   2. 🎨 Affichage dans un cadre Unicode          │
│                                                  │
│   3. 💾 Proposition de sauvegarde                │
│                                                  │
└──────────────────────────────────────────────────┘
```

### 🌐 API utilisée

Le script utilise l'API **Kaamelott** :
- **URL** : `https://kaamelott.chaudie.re/api/random`
- **Méthode** : GET
- **Authentification** : Aucune (gratuit et public)
- **Documentation** : [GitHub - api-kaamelott](https://github.com/sin0light/api-kaamelott)

### 📚 Mode hors-ligne

Si l'API est inaccessible (pas de connexion, timeout, erreur serveur), le script bascule automatiquement sur des citations locales françaises :

```
🔍 Recherche d'une réplique culte...
📚 Mode hors-ligne — réplique locale

╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║  Le succès, c'est se promener d'échec en échec [...] — W. Churchill   ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
```

---

## 🛡️ Sécurité

Le script intègre plusieurs protections :

| Protection | Description |
|------------|-------------|
| 🚫 **Path Traversal** | Impossible d'écrire en dehors du dossier courant |
| ✅ **Validation JSON** | Vérification du format de réponse de l'API |
| 🔄 **Fallback garanti** | Le script ne plante jamais, même sans Internet |
| 📝 **Encodage UTF-8** | Support des caractères spéciaux (accents, émojis) |

---

## 📁 Structure du projet

```
inspire_me/
├── inspire_me.py     # 🐍 Script principal
├── citation.txt      # 💾 Fichier généré (si sauvegarde)
└── README.md         # 📖 Ce fichier
```

---

## ⚙️ Configuration

Les constantes sont configurables en haut du fichier `inspire_me.py` :

```python
# API
API_URL: str = "https://kaamelott.chaudie.re/api/random"
API_TIMEOUT: int = 5  # Secondes

# Fichier de sortie
FICHIER_SORTIE: str = "citation.txt"

# Réponses acceptées pour la sauvegarde
REPONSES_POSITIVES: set[str] = {"o", "oui", "y", "yes"}
```

---

## 🎭 Exemples de répliques

Voici quelques perles que vous pourriez obtenir :

> *"C'est pas faux."* — **Perceval**

> *"On en a gros !"* — **Perceval**

> *"Le gras, c'est la vie."* — **Karadoc**

> *"Faut arrêter ces conneries de la Table Ronde."* — **Arthur**

> *"Mais vous êtes pas mort ? — Ben si, mais à moitié."* — **Le Répurgateur**

---

## 🐛 Dépannage

### Le script affiche toujours "Mode hors-ligne"

1. Vérifiez votre connexion Internet
2. L'API Kaamelott est peut-être temporairement indisponible
3. Le fallback local fonctionne quand même ! ✅

### Erreur "Permission denied" à la sauvegarde

Vérifiez que vous avez les droits d'écriture dans le dossier courant.

### Caractères bizarres dans le terminal

Assurez-vous que votre terminal supporte l'UTF-8 et les caractères Unicode.

---

## 📜 Licence

Ce projet est libre d'utilisation. L'API Kaamelott est maintenue par [sin0light](https://github.com/sin0light/api-kaamelott).

*Kaamelott est une série créée par Alexandre Astier.*

---

## 🙏 Crédits

- **API Kaamelott** : [kaamelott.chaudie.re](https://kaamelott.chaudie.re/)
- **Série Kaamelott** : Alexandre Astier & CALT Production
- **Développement** : Créé avec le swarm Architecte/Développeur/Testeur 🤖

---

## 🚀 Évolutions possibles

- [ ] 🎯 Filtrer par personnage (`--personnage Perceval`)
- [ ] 📖 Filtrer par livre/saison (`--livre 1`)
- [ ] 📜 Historique des citations affichées
- [ ] 🖼️ Version avec interface graphique (Tkinter)
- [ ] 📦 Packaging en `.exe` pour Windows

---

<p align="center">
  <i>« C'est pas faux. »</i><br>
  <b>— Perceval de Galles</b>
</p>

<p align="center">
  ⚔️ Fait avec ❤️ et beaucoup de citations de Kaamelott ⚔️
</p>
