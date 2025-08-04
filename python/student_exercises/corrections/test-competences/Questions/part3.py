"""
Les données sont en format list de dictionnaires;
Ou les dictionnaires sont du format suivant:
  - "nom": str
  - "notes": dict[str, list[int]]
ou le nom est une chaîne de caractères qui donne le nom de l'etuudiant et
les notes sont un dictionnaire comme suit:
  - "matiere": list[int]
ou la clé du dicionnaire est le nom de la matière et la valeur est une liste de notes
"""

donnees: list[dict[str, str | dict[str, list[int]]]] = [
    {"nom": "Alice", "notes": {"math": [4, 5], "francais": [6], "anglais": [3]}},
    {"nom": "Bob", "notes": {"math": [1], "francais": [5], "anglais": [2]}},
    {"nom": "Clara", "notes": {"math": [5], "francais": [6], "anglais": [4]}},
]


def calculer_moyenne_etudiants(
    donnees: list[dict[str, str | dict[str, list[int]]]],
) -> dict[str, float]:
    """
    Calcule la moyenne de chaque étudiant, arrondie au centième.

    Args:
      donnees (list[dict[str, str | dict[str, list[int]]]]): Liste de dictionnaires avec nom et notes.

    Returns:
      dict: nom -> moyenne

    Exemples:
      >>> calculer_moyenne_etudiants(donnees)
      {'Alice': 4.5, 'Bob': 2.67, 'Clara': 5.0}
    """
    res: dict[str, float] = {}
    for d in donnees:
        sum_ = 0
        nb_grades = 0
        for g in d["notes"].values():
            sum_ += sum(g)
            nb_grades += len(g)
        res[d["nom"]] = round(sum_ / nb_grades, 2)
    return res


def meilleur_etudiant(moyennes: dict[str, float]) -> tuple[str, float]:
    """
    Retourne le nom du meilleur étudiant et sa moyenne.

    Args:
      moyennes (dict): nom -> moyenne

    Returns:
      tuple: (nom, moyenne)

    Exemples:
      >>> meilleur_etudiant({'Alice': 14.33, 'Bob': 10.33, 'Clara': 18.0})
      ('Clara', 18.0)
    """
    max_student = max(moyennes, key=moyennes.get)
    return max_student, moyennes.get(max_student)


def ajouter_note(
    donnees: list[dict[str, str | dict[str, list[int]]]],
    nom: str,
    matiere: str,
    note: int,
) -> list[dict[str, str | dict[str, list[int]]]]:
    """
    Ajoute une note d’un étudiant pour une matière.

    Args:
      donnees (list): Données des étudiants.
      nom (str): Nom de l’étudiant.
      matiere (str): Nom de la matière.
      note (int): Note à ajouter.

    Returns:
      list: Données des étudiants modifiées.

    Exemples:
      >>> ajouter_note(donnees, "Clara", "math", 4)
      [
        {"nom": "Alice", "notes": {"math": [4, 5], "francais": [6], "anglais": [3]}},
        {"nom": "Bob", "notes": {"math": [1], "francais": [5], "anglais": [2]}},
        {"nom": "Clara", "notes": {"math": [5, 4], "francais": [6], "anglais": [4]}},
      ]

      >>> ajouter_note(donnees, "Clara", "physique", 5)
      [
        {"nom": "Alice", "notes": {"math": [4, 5], "francais": [6], "anglais": [3]}},
        {"nom": "Bob", "notes": {"math": [1], "francais": [5], "anglais": [2]}},
        {"nom": "Clara", "notes": {"math": [5], "francais": [6], "anglais": [4], "physique": [5]}},
      ]
    """
    found_student: bool = False
    for d in donnees:
        if d["nom"] == nom:
            found_student = True
            d["notes"][matiere] = d["notes"].get(matiere, []) + [note]
    if not found_student:
        donnees.append({"nom": nom, "notes": {matiere: note}})
    return donnees
