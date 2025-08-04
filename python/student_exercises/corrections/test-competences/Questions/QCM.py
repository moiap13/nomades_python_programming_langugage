# Cette partie est un QCM, Les questions seront posés en commentaire
# Chaques questions à une seule bonne réponse parmis les 4 proposées
# Une variable qcm_answer est définie comme un tableau de int
# Chaque index du tableau correspond à une question et la valeur correspond à la réponse choisie
# Par défaut la valuer est None, il faut remplacer None par le numéro de la réponse choisie
# Une bonne réponse rapporte 1 point, une mauvaise réponse rapporte 0 point
# Une réponse non donnée (None) rapporte 0 point
# Exemple: qcm_answer = [1, 2, 3, 4, 1, 2, 3, 4]
# Ici, la réponse à la première question est la réponse 1, la réponse à la deuxième question est la réponse 2, etc...

NB_QUESTIONS = 35
qcm_answers = [None] * NB_QUESTIONS

################################################################################
# 0. Quel est le type de la variable qcm_answer ?
# 1. int
# 2. float
# 3. str
# 4. list

qcm_answers[0] = 4


################################################################################
# 1. Quel est l'output de la fonction f()
def f():
    numbers = [1, 2, 3, 4, 5]
    squared_numbers = [x**2 for x in numbers]
    print(squared_numbers)


# 1. [1, 2, 3, 4, 5]
# 2. [1, 4, 9, 16, 25]
# 3. [2, 4, 6, 8, 10]
# 4. [1, 8, 27, 64, 125]

qcm_answers[1] = 2

################################################################################
# 2. Quel mot clé permet de définir une classe en python ?
# 1. class
# 2. def
# 3. new
# 4. object

qcm_answers[2] = 1

################################################################################
# 3. Lequel de ces types et un type immutable ?
# 1. list
# 2. dict
# 3. tuple
# 4. set

qcm_answers[3] = 3

################################################################################
# 4. Quel est l'utilité de `Try`...`Except` en Python ?
# 1. Ca définit une boucle
# 2. Ca permet de gérer les exceptions
# 3. Ca permet de break une boucle
# 4. Ca permet de brancher le code

qcm_answers[4] = 2

################################################################################
# 5. Quel est l'utilité de la fonction `__init__` dans une classe ?
# 1. Une fonction qui permet de supprimer une classe
# 2. Une fonction qui permet de copier une classe
# 3. Une fonction qui permet de comparer deux classes
# 4. Une fonction qui permet d'initialiser une classe

qcm_answers[5] = 4

################################################################################
# 6. En python, quel est l'utilité principale d'un Set ?
# 1. Ca permet de stocker des valeurs uniques
# 2. Ca permet de stocker des valeurs ordonnées
# 3. Ca permet de stocker des valeurs sous la fomr clé/valeur
# 4. Ca permet de stocker des valuers afin que la recherche soit plus rapide (b-tree)

qcm_answers[6] = 1

################################################################################
# 7. Que fait la fonction `split()` sur une chaine de caractère qui réprésente une phrase (avec des espaces) ?
# 1. Ca remplace les espaces par des virgules
# 2. Ca découpe la chaine de caractère en une liste de caractères
# 3. Ca supprime les espaces en début et fin de chaine
# 4. Ca découpe la chaine de caractère en une liste de mots

qcm_answers[7] = 4


################################################################################
# 8. Quel est le type de retour de la foncition suivante ?
def f():
    return 1, 2, 3


# 1. int
# 2. float
# 3. str
# 4. tuple

qcm_answers[8] = 4

################################################################################
# 9. Ayant les deux variables suivantes :
keys = ["key1", "key2", "key3"]
values = ["value1", "value2", "value3"]

# Quelles method n'est pas une méthode valide pour créer un dictionnaire ?
# 1. dict(zip(keys, values))
# 2. {k: v for k, v in zip(keys, values)}
# 3. dict(keys, values)
# 4. dict.fromkeys(keys, values)

qcm_answers[9] = 3

################################################################################
# 10. Que fait le mot clé `pass` ?
# 1. Arrête l'execution du code
# 2. Lève une exception
# 3. Ne fait rien
# 4. Stop la boucle

qcm_answers[10] = 3

################################################################################
# 11. Quelle fonction `built-in` permet de connaître la taille d'un itérable ?
# 1. size()
# 2. length()
# 3. len()
# 4. count()

qcm_answers[11] = 3

################################################################################
# 12. Quelle methode ne permet pas de créer un Tuple en python ?
# 1. (1, 2, 3)
# 2. tuple([1, 2, 3])
# 3. (1)
# 4. (1,)

qcm_answers[12] = 3

################################################################################
# 13. Quelle fonction permet de créer un Set en python ?
# 1. set()
# 2. {}
# 3. new Set()
# 4. (1, 2, 3)

qcm_answers[13] = 1

################################################################################
# 14. Quel est l'utilité de la fonction `__str__` dans une classe en Python ?
# 1. Une fonction qui permet de convertir une string en classe
# 2. Une fonction qui verifie si une classe est une string
# 3. Une fonction qui crée une nouvelle chain de caractère
# 4. Une fonction qui permet de convertir une classe en string

qcm_answers[14] = 4

################################################################################
# 15. Quel methode est plus performante pour créer un dictionnaire vide ?
# 1. dict()
# 2. {}
# 3. Les deux sont équivalents
# 4. Il n'est pas possible de créer un dictionnaire vide

qcm_answers[15] = 2


################################################################################
# 16. Etant donné ce code :
class A:
    def __init__(self):
        self.a = 1

    def say_hello(self):
        print("Hello")


class B(A):
    def __init__(self):
        super().__init__()
        self.b = 2

    def say_hello(self):
        print("Bonjour")


class C:
    def __init__(self):
        self.c = 3

    def say_hello(self):
        print("Hola")


class D(C, B):
    def __init__(self):
        super().__init__()
        self.d = 4


d = D()

# Quel serait l'output de `d.say_hello()` ?
# 1. Hello
# 2. Bonjour
# 3. Une erreur est levée
# 4. Hola

qcm_answers[16] = 4

################################################################################
# 17. Quelle boucle n'existe pas en Python ?
# 1. for
# 2. do-while
# 3. while
# 4. elles existent toutes

qcm_answers[17] = 2

################################################################################
# 18. Quel terme définit le code suitant ?
count, fruit, price = (2, "apple", 3.5)
# 1. Tuple unpacking
# 2. Tuple packing
# 3. Tuple assignment
# 4. Tuple matching

qcm_answers[18] = 1

################################################################################
# 19. Quel est le runtime d'accès à un élément dans un dictionnaire par sa clé ?
# 1. O(n), aussi appellé `linear time`.
# 2. O(log n), aussi appellé `logarithmic time`.
# 3. O(n^2), aussi appellé `quadratic time`.
# 4. O(1), aussi appellé `constant time`.

qcm_answers[19] = 4

################################################################################
# 20. Quel est la bonne syntaxe pour définir une classe `Game` qui hérite de la classe parente `LogicGame` ?
# 1. def Game(LogicGame): pass
# 2. class Game(LogicGame): pass
# 3. def Game.LogicGame(): pass
# 4. class Game.LogicGame(): pass

qcm_answers[20] = 2

################################################################################
# 21. Quel est la bonne façon pour définir une instance de la classe `Game` ?
# 1. my_game = class.Game()
# 2. my_game = class(Game)
# 3. my_game = Game()
# 4. my_game = Game.create()

qcm_answers[21] = 3

################################################################################
# 22. Si on ecrit PAS explicitement le mot clé `return` a la fin d'une fonction, quelle est la valeur de retour de la fonction ?
# 1. La fonction retournera l'exeption `ReturnError`
# 2. Si la fonction ne retourne rien, elle retourne `None`
# 3. Si la fonction ne retourne rien, elle retourne `True`
# 4. La fonction entre dans une boucle infinie, car ele ne sait pas quand il faut retourner

qcm_answers[22] = 2

################################################################################
# 23. Suivant le code suivant :
fruit_info = {"fruit": "apple", "count": 2, "price": 3.5}
# 26. Quel est la syntaxe correcte pour changer le prix de 3.5 à 1.5 ?
# 1. fruit_info['price'] = 1.5
# 2. fruit_info[2] = 1.5
# 3. fruit_info[price] = 1.5
# 4. fruit_info.price = 1.5

qcm_answers[23] = 1

################################################################################
# 24. Quelle valeure est retournée par l'instruction suivante: `5 != 6` ?
# 1. Yes
# 3. True
# 4. False
# 2. None

qcm_answers[24] = 3

################################################################################
# 25. Pourquoi c'est une bonne pratique d'ouvrir des fichiers avec le mot clé `with` ?

# 1. Le mot clé `with` permet de choisir avec quelle application on aimerait ouvrir le fichier
# 2. Le mot clé `with` est utilisé comme une boucle `for` et permet de lire le fichier ligne par ligne
# 3. Il n'y a pas de bénéfice à utiliser le mot clé `with` pour ouvrir un fichier
# 4. Le mot clé `with` permet de fermer le fichier automatiquement après la fin du bloc

qcm_answers[25] = 4

################################################################################
# 26. À quoi sert le slicing ?
# 1. Supprimer des valeurs
# 2. Filtrer des types
# 3. Extraire des sous-chaînes/sous-listes
# 4. Créer des classes

qcm_answers[26] = 3

################################################################################
# 27. Quelle est une f-string valide ?
# 1. f"Bonjour {nom}"
# 2. "f'Bonjour {nom}'"
# 3. "f(Bonjour, nom)"
# 4. format("Bonjour {}", nom)

qcm_answers[27] = 1

################################################################################
# 28. Que retourne [x for x in range(5) if x % 2 == 0] ?
# 1. [1, 2, 3, 4]
# 2. [0, 2, 4]
# 3. [1, 3, 5]
# 4. [2, 4]

qcm_answers[28] = 2

################################################################################
# 29. Que retourne enumerate(['a', 'b', 'c']) ?
# 1. ['a', 'b', 'c']
# 2. [(0, 'a'), (1, 'b'), (2, 'c')]
# 3. {0: 'a', 1: 'b', 2: 'c'}
# 4. Un objet type range

qcm_answers[29] = 2

################################################################################
# 30. Quel est le résultat de [1, 2, 3][-1] ?
# 1. 1
# 2. 3
# 3. -1
# 4. Erreur

qcm_answers[30] = 2

################################################################################
# 31. Quel est le type de retour de la fonction input() ?
# 1. int
# 2. str
# 3. bool
# 4. dépend de l'entrée

qcm_answers[31] = 2

################################################################################
# 32. Que retourne list(range(1, 5)) ?
# 1. [1, 2, 3, 4, 5]
# 2. [0, 1, 2, 3, 4]
# 3. [1, 2, 3, 4]
# 4. [1, 2, 3, 4, 5, 6]

qcm_answers[32] = 3
