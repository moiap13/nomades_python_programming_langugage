# Test de compétences python

Vous effectuez un test de compétences, cette première partie est un test de compétences sur les bases de python.
Les test se divise en 3 petits tests:
- Test 0: Un QCM de 33 questions
- Test 1: implementation de petites fonction en python
- Test 2: implementation plus pratique sur un calcul de notes

## Test 0

Cette partie est un QCM, Les questions seront posés en commentaire, chaques questions à une seule bonne réponse parmis les 4 proposées. Une variable `qcm_answer` est définie comme un tableau de int et chaque index du tableau correspond à une question et la valeur correspond à la réponse choisie.
Par défaut la valuer est None, *il faut remplacer None par le numéro de la réponse choisie*
Une bonne réponse rapporte 1 point, une mauvaise réponse rapporte 0 point, une réponse non donnée (None) rapporte 0 point
*Exemple:* 
```python 
qcm_answer = [1, 2, 3, 4, 1, 2, 3, 4]
```
Ici, la réponse à la première question est la réponse 1, la réponse à la deuxième question est la réponse 2, etc...

## Test 1

Le Test 1 se trouve dans le fichier [part2.py](Questions/part2.py), vous devez remplir les fonctions `frequence_mots`, `annee_bissextile`, `trouver_maximum`, `est_palindrome` et `retirer_doublons` en python, vous avez le droit d'utiliser les fonctions de la libraire standard de python sauf quand le contraire est renseigné.

## Test 2

Le Test 2 se trouve dans le fichier [part3.py](Questions/part3.py), vous devez remplir les fonctions `calculer_moyenne_etudiants`, `meilleur_etudiant` et `ajouter_note`. cet exerice est plus pratique et vous avez le droit d'utiliser les fonctions de la libraire standard de python sauf quand le contraire est renseigné.

> Lisez bien les instructions pour bien comprendre ce qu'il faut faire

> Vous avez 2h pour terminer le test

Les tests seront tester et corrigé automatiqeument grâce à des tests unitaires