#!/usr/bin/env python3
"""
inspire_me.py — Générateur de citations inspirantes.

Ce script récupère une citation depuis l'API quotable.io,
avec fallback sur des citations locales en cas d'échec.
"""

from __future__ import annotations  # Compatibilité Python 3.7+

from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
import json
import random
import ssl

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTES
# ═══════════════════════════════════════════════════════════════════════════════
CITATIONS: list[str] = [
    "Le succès, c'est se promener d'échec en échec tout en restant motivé. — Winston Churchill",
    "La vie, c'est comme une bicyclette, il faut avancer pour ne pas perdre l'équilibre. — Albert Einstein",
    "Ce n'est pas parce que les choses sont difficiles que nous n'osons pas, c'est parce que nous n'osons pas qu'elles sont difficiles. — Sénèque",
    "Le seul voyage impossible est celui que vous ne commencez jamais. — Tony Robbins",
    "La créativité, c'est l'intelligence qui s'amuse. — Albert Einstein",
]

# Fallback ultime si CITATIONS est vide
CITATION_DEFAUT: str = "La persévérance est la clé du succès. — Anonyme"

FICHIER_SORTIE: str = "citation.txt"
REPONSES_POSITIVES: set[str] = {"o", "oui", "y", "yes"}

# Configuration API
API_URL: str = "https://kaamelott.chaudie.re/api/random"
API_TIMEOUT: int = 5
API_USER_AGENT: str = "Mozilla/5.0 (compatible; inspire_me/2.0; +https://github.com)"

# Messages utilisateur
MSG_CHARGEMENT: str = "🔍 Recherche d'une réplique culte..."
MSG_HORS_LIGNE: str = "📚 Mode hors-ligne — réplique locale"


# ═══════════════════════════════════════════════════════════════════════════════
# 1. SÉLECTION LOCALE (conservée pour fallback)
# ═══════════════════════════════════════════════════════════════════════════════
def choisir_citation(citations: list[str]) -> str:
    """
    Sélectionne une citation au hasard dans la liste fournie.

    Args:
        citations: Liste de citations parmi lesquelles choisir.

    Returns:
        Une citation sélectionnée aléatoirement.

    Raises:
        ValueError: Si la liste de citations est vide.
    """
    if not citations:
        raise ValueError("Aucune citation disponible.")
    return random.choice(citations)


# ═══════════════════════════════════════════════════════════════════════════════
# 2. FONCTIONS API (NOUVELLES)
# ═══════════════════════════════════════════════════════════════════════════════
def requete_api(url: str, timeout: int = API_TIMEOUT) -> dict | None:
    """
    Effectue une requête GET vers l'API.

    Args:
        url: URL de l'API.
        timeout: Délai maximum en secondes.

    Returns:
        dict: Réponse JSON parsée si succès.
        None: En cas d'échec.

    Exceptions gérées silencieusement:
        - HTTPError: Erreur serveur (4xx, 5xx)
        - URLError: Pas de connexion / DNS
        - TimeoutError: Délai dépassé
        - ssl.SSLError: Certificat invalide
        - json.JSONDecodeError: Réponse non-JSON
    """
    try:
        context = ssl.create_default_context()
        request = Request(url, headers={"User-Agent": API_USER_AGENT})

        with urlopen(request, timeout=timeout, context=context) as response:
            return json.loads(response.read().decode("utf-8"))

    except (HTTPError, URLError, TimeoutError, ssl.SSLError, json.JSONDecodeError):
        return None
    except Exception:
        return None


def extraire_citation_json(data: dict) -> str | None:
    """
    Extrait et valide la citation depuis la réponse JSON de l'API Kaamelott.

    Format attendu:
        {
          "status": 1,
          "citation": {
            "citation": "Le texte...",
            "infos": {
              "personnage": "Perceval",
              ...
            }
          }
        }

    Args:
        data: Dictionnaire JSON de l'API.

    Returns:
        str: Citation formatée "texte — Personnage"
        None: Si format invalide ou status != 1
    """
    try:
        # Vérifier le statut
        if data.get("status") != 1:
            return None

        citation_data = data.get("citation") or {}

        texte = citation_data.get("citation") or ""
        texte = texte.strip()

        if not texte:
            return None

        # Extraire le personnage depuis infos
        infos = citation_data.get("infos") or {}
        personnage = infos.get("personnage") or ""
        personnage = personnage.strip()

        if personnage:
            return f"{texte} — {personnage}"
        else:
            return texte

    except (AttributeError, TypeError):
        return None


def obtenir_citation() -> str:
    """
    Obtient une citation depuis l'API ou le fallback local.

    Workflow:
        1. Affiche message de chargement
        2. Tente requête API quotable.io
        3. Valide et extrait la citation du JSON
        4. En cas d'échec → fallback CITATIONS locales
        5. Si CITATIONS vide → fallback CITATION_DEFAUT
        6. Applique sanitizer_citation() dans TOUS les cas

    Returns:
        str: Citation prête à afficher (toujours sanitizée).

    Garantie: Ne lève JAMAIS d'exception.
    """
    print(MSG_CHARGEMENT)

    # Tentative API
    data = requete_api(API_URL)

    if data is not None:
        citation = extraire_citation_json(data)
        if citation is not None:
            return sanitizer_citation(citation)

    # Fallback local
    print(MSG_HORS_LIGNE)

    try:
        citation = choisir_citation(CITATIONS)
    except ValueError:
        citation = CITATION_DEFAUT

    return sanitizer_citation(citation)


# ═══════════════════════════════════════════════════════════════════════════════
# 3. SANITIZATION
# ═══════════════════════════════════════════════════════════════════════════════
def sanitizer_citation(citation: str) -> str:
    """
    Nettoie une citation des caractères qui casseraient le cadre.

    Remplace les sauts de ligne et tabulations par des espaces,
    puis normalise les espaces multiples.

    Args:
        citation: La citation brute.

    Returns:
        La citation nettoyée.
    """
    # Remplacer \n, \r, \t par des espaces
    citation = citation.replace("\n", " ").replace("\r", " ").replace("\t", " ")
    # Normaliser les espaces multiples
    citation = " ".join(citation.split())
    return citation


# ═══════════════════════════════════════════════════════════════════════════════
# 4. AFFICHAGE
# ═══════════════════════════════════════════════════════════════════════════════
def afficher_citation(citation: str) -> None:
    """
    Affiche la citation dans un cadre Unicode décoratif.

    Le cadre s'adapte dynamiquement à la longueur de la citation.

    Args:
        citation: La citation à afficher.

    Raises:
        ValueError: Si la citation est vide après nettoyage.
    """
    # Nettoyage de la citation
    citation = sanitizer_citation(citation)

    # Validation citation non vide
    if not citation:
        raise ValueError("La citation ne peut pas être vide.")

    # Calcul de la largeur du cadre
    largeur_interieure = len(citation) + 4  # 2 espaces de padding de chaque côté

    # Construction du cadre
    ligne_haut = "╔" + "═" * largeur_interieure + "╗"
    ligne_bas = "╚" + "═" * largeur_interieure + "╝"
    ligne_vide = "║" + " " * largeur_interieure + "║"
    ligne_citation = "║  " + citation + "  ║"

    # Affichage
    print()
    print(ligne_haut)
    print(ligne_vide)
    print(ligne_citation)
    print(ligne_vide)
    print(ligne_bas)
    print()


# ═══════════════════════════════════════════════════════════════════════════════
# 5. VALIDATION ENTRÉE UTILISATEUR
# ═══════════════════════════════════════════════════════════════════════════════
def confirmer_sauvegarde() -> bool:
    """
    Demande confirmation à l'utilisateur pour sauvegarder la citation.

    Returns:
        True si la réponse est dans REPONSES_POSITIVES (insensible à la casse).
        False pour toute autre entrée (y compris vide).
    """
    reponse = input("Voulez-vous sauvegarder cette citation ? (o/n) : ")
    return reponse.strip().lower() in REPONSES_POSITIVES


# ═══════════════════════════════════════════════════════════════════════════════
# 6. VALIDATION CHEMIN FICHIER
# ═══════════════════════════════════════════════════════════════════════════════
def valider_chemin(fichier: str) -> Path:
    """
    Valide et sécurise le chemin du fichier.

    Résout le chemin absolu et vérifie qu'il reste dans le répertoire courant
    pour prévenir les attaques de type path traversal.

    Args:
        fichier: Nom ou chemin du fichier à valider.

    Returns:
        Path: Chemin sécurisé et validé.

    Raises:
        ValueError: Si le chemin tente de sortir du répertoire courant.
    """
    chemin_absolu = Path(fichier).resolve()
    repertoire_courant = Path.cwd().resolve()

    if not chemin_absolu.is_relative_to(repertoire_courant):
        raise ValueError(
            f"Chemin non autorisé : le fichier doit rester dans {repertoire_courant}"
        )

    return chemin_absolu


# ═══════════════════════════════════════════════════════════════════════════════
# 7. SAUVEGARDE
# ═══════════════════════════════════════════════════════════════════════════════
def sauvegarder_citation(citation: str, fichier: str = FICHIER_SORTIE) -> bool:
    """
    Sauvegarde la citation dans un fichier texte.

    Args:
        citation: La citation à sauvegarder.
        fichier: Nom du fichier de sortie (défaut: citation.txt).

    Returns:
        True si la sauvegarde a réussi, False sinon.
    """
    try:
        chemin = valider_chemin(fichier)
        with open(chemin, "w", encoding="utf-8") as f:
            f.write(citation + "\n")
        return True
    except OSError as e:
        print(f"Erreur lors de la sauvegarde : {e}")
        return False


# ═══════════════════════════════════════════════════════════════════════════════
# 8. ORCHESTRATION
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> None:
    """
    Point d'entrée principal du script.

    Orchestre le flux complet : récupération (API ou fallback),
    affichage, et sauvegarde optionnelle.
    """
    try:
        # Obtention de la citation (API ou fallback)
        citation = obtenir_citation()

        # Affichage
        afficher_citation(citation)

        # Proposition de sauvegarde
        if confirmer_sauvegarde():
            if sauvegarder_citation(citation):
                print(f"✓ Citation sauvegardée dans '{FICHIER_SORTIE}'")
            else:
                print("✗ La sauvegarde a échoué.")
        else:
            print("Sauvegarde annulée.")

    except ValueError as e:
        print(f"Erreur : {e}")
    except KeyboardInterrupt:
        print("\n\nInterruption. À bientôt !")


# ═══════════════════════════════════════════════════════════════════════════════
# POINT D'ENTRÉE
# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    main()
