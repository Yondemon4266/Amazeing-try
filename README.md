# 🌀 A-Maze-Ing

**A-Maze-Ing** est un moteur de génération et de résolution de labyrinthes conçu en Python. Ce projet met l'accent sur la modularité avec un générateur autonome (`MazeGenerator`) capable de produire des structures complexes (parfaites ou imparfaites) et d'en extraire la solution optimale.

---

## 📅 Anticipated Planning & Development Strategy

Cette section retrace la réflexion derrière la conception du projet et son évolution technique.

### Phase 1 : Configuration & Robustesse
Le point d'entrée est le moteur de **Parsing & Validation**. 
* **Source :** `config.txt`.
* **Logique :** Implémentation d'un validateur strict pour s'assurer que les paramètres (largeur, hauteur, graine, etc.) sont cohérents. Un labyrinthe ne peut être généré si les dimensions sont absurdes ou si les contraintes sont physiquement impossibles.
* **Objectif :** Échouer rapidement avec des messages d'erreur clairs plutôt que de s'exécuter avec des données corrompues.

### Phase 2 : Représentation des données (Bitmasking)
Pour garantir la performance, le labyrinthe est représenté par un **tableau 1D d'entiers**.
* **Encodage :** Chaque cellule est un entier de `0` à `15`.
* **État initial :** Toutes les cellules sont initialisées à `15` ($1111$ en binaire), représentant une cellule où les quatre murs sont fermés.
* **Bénéfices :** Cette approche par bitmasking permet une manipulation extrêmement rapide des murs via des opérateurs binaires et une structure mémoire optimisée.



### Phase 3 : Moteur de génération (MazeGenerator)
La logique centrale est encapsulée dans un module autonome.
* **Algorithme :** **Algorithme de Prim**. Contrairement au DFS (Depth-First Search) qui crée de longs couloirs sinueux, Prim tend à créer des structures plus organiques et ramifiées.
* **Entrée/Sortie :** Sélection aléatoire des points d'entrée et de sortie sur les bordures, en s'assurant qu'ils sont distincts.
* **Parfait vs Imparfait :** * *Parfait :* L'algorithme garantit un chemin unique entre deux points (Spanning Tree).
    * *Imparfait :* Une phase post-génération supprime sélectivement des murs pour créer des boucles.

### Phase 4 : Résolution & Interaction
* **Solver :** Implémentation d'un parcours en largeur (BFS) pour trouver le chemin le plus court (solution optimale).
* **UX :** Interface terminale interactive permettant de visualiser le labyrinthe, ses caractéristiques et sa solution.

---

## 🏗 Structure du Projet

Le générateur est implémenté comme un package autonome (`standalone`) pour être réutilisé dans de futurs projets.

```text
.
├── main.py                 # Script principal / UI
├── config.txt              # Fichier de configuration
└── MazeGenerator/          # Module réutilisable
    ├── __init__.py         # Initialisation du package
    ├── generator.py        # Classe MazeGenerator
    └── maze_structure.py   # Classe de données Maze