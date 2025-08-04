max = None


def frequence_mots(texte: str) -> dict[str, int]:
    """
    Retourne un dictionnaire avec les frequences des caractères
    (seulement les lettres, pas de chiffres ou caratères speciaux)

    Args:
      texte (str): Texte brut.

    Returns:
      dict: {mot: fréquence}

    Exemples:
      >>> frequence_mots("Bonjour le monde")
      {'B': 1, 'o': 2, 'n': 2, 'j': 1, 'u': 1, 'r': 2, 'l': 1, 'e': 3, 'm': 1, 'd': 1}
    """
    res: dict[str, int] = {}
    for c in texte:
        if c.isalpha():
            res[c] = res.get(c, 0) + 1
    return res


def annee_bissextile(annee: int) -> bool:
    """
    Retourne True si l'annee est bissextile, False sinon.
    Une annee est bissextile si elle est divisible par 4 mais pas par 100
    ou si elle est divisible par 400

    Args:
      annee (int): L'annee.

    Returns:
      bool: True si l'annee est bissextile, False sinon.

    Exemples:
      >>> annee_bissextile(2020)
      True
      >>> annee_bissextile(2021)
      False
      >>> annee_bissextile(1900)
      False
    """
    return annee % 4 == 0 and (annee % 100 != 0 or annee % 400 == 0)


def trouver_maximum(numbers: list[int]) -> int:
    """
    Trouve la valeur maximale dans une liste.
    sans utiliser la fonction max de python

    Args:
      numbers (list): Liste de nombres.

    Returns:
      int/float: La plus grande valeur.

    Exemples:
      >>> trouver_maximum([1, 2, 3, 4, 5])
      5
    """
    if not numbers:
        raise ValueError

    max = numbers[0]
    for i in range(1, len(numbers)):
        if numbers[i] > max:
            max = numbers[i]
    return max


def est_palindrome(chaine: str) -> bool:
    """
    Vérifie si une chaîne est un palindrome.

    Args:
      chaine (str): La chaîne à vérifier.

    Returns:
      bool: True si palindrome, False sinon.

    Exemples:
      >>> est_palindrome("radar")
      True
      >>> est_palindrome("hello")
      False
    """
    return chaine == chaine[::-1]


def retirer_doublons(liste: list[any]) -> list[any]:
    """
    Retire les doublons d'une liste tout en gardant l'ordre.

    Args:
      liste (list): Liste avec possibles doublons.

    Returns:
      list: Liste sans doublons.

    Exemples:
      >>> retirer_doublons([1, 2, 2, 3, 4, 4, 5])
      [1, 2, 3, 4, 5]
    """
    uniques: list[any] = []

    for i in liste:
        if i not in uniques:
            uniques.append(i)
    return uniques
