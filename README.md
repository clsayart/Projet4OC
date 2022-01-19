# OCR_P4 - Projet P4 - Développez un programme logiciel en Python
### Création d'un logiciel pour le tournoi d'un club d'échec
***
## Présentation


A été demandé, la réalisation d'un logiciel permettant de réaliser un tournoi d'échec, entre huits joueurs avec la réalisation de quatres tours
de jeu pour déterminer le gagnant du tournoi.
L'utilisateur peut inscrire les joueurs dans une base de données (tinydb), générer les
quatres tours de jeu, et exporter différents résultats dans la console
***
## Prérequis : 
[![made-with-python](
https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](
https://www.python.org/)
[![Python badge](https://img.shields.io/badge/Python->=3.9.9-blue.svg)](
https://www.python.org/)
***
## Clonage du Repository :
````shell
git clone https://github.com/clsayart/Projet4OC
````
***
## Environnement Virtuel :
création de l'environnement virtuel
```shell
python3 -m venv [nom_de_votre_environnement_virtuel] 
```
activation de l'environnement virtuel
### Mac/Linux
````shell
source [nom_de_votre_environnement_virtuel]/bin/activate
````
### Windows
````shell
source .\[nom_de_votre_environnement_virtuel]\Scripts\activate
````

Aller dans le dossier OCR_P4 contenant les fichiers
```shell
cd pythonProject3 - Copie 
```
***
## Installation des packages nécessaires
````shell
pip install -r requirements.txt 
````
***
## Lancement du programme : 
Exécution du Programme via le fichier principal : main.py présent dans le 
dossier OCR_P4
````shell
python3 main.py 
````
Cette commande produit le resultat suivant : 

"----------Tournoi----------"
1. Start Tournoi - Please enter 1"
2. View Rapports - Please enter 2"
en effet, le programme dispose d'une interface dans le terminal. 

```shell
 ###Génération Rapport Flake8

Après avoir activé l'environnement virtuel, entrez la commande suivante :

flake8 --format=html --htmldir=flake_rapport

flake8 --format=html --htmldir=flake_rapport --exclude venv

```
Un rapport sera généré dans le dossier "flake_rapport", avec comme argument 
"max-line-length" défini par défaut à 79 caractères par ligne si non précisé.
