# Modèle Quarto pour les cours : livre et présentations

## Principe

Chaque cours et le modèle peuvent être des dépôts Git indépendants. Les fichiers du modèle sont **copiés** dans chaque cours : aucun lien extérieur au dépôt n’est requis pour son rendu.

La séparation est faite dans les fichiers YAML : les informations du cours restent dans `_quarto.yml`, la présentation et les fonctionnalités réutilisables dans `_template.yml`. Quarto les combine avec son mécanisme natif `metadata-files`.

Il n’y a pas de gestionnaire de synchronisation Python, de manifeste, de verrou, de répertoire `_teaching/`, de submodule ou de subtree configuré.

## Structure habituelle

```text
mon-cours/
├── _quarto.yml                 ← réglages propres au cours
├── _template.yml               ← réglages partagés du livre
├── _quarto-answer.yml
├── _quarto-question.yml
├── index.qmd
├── assets/                     ← styles, scripts web, CSL, bibliographie
├── _extensions/                ← extensions du livre
├── scripts/                    ← construction des supports
├── course/
│   ├── class_01.qmd
│   └── class_02.qmd
└── slides/
    ├── _quarto.yml             ← réglages propres aux slides de ce cours
    ├── _template.yml           ← thème et plugins réutilisables des slides
    ├── _extensions/            ← clean, animate, verticator, etc.
    ├── assets/
    ├── mathjax-config.js
    └── slides_class_01.qmd
```

`course/` et `slides/` sont les deux dossiers de contenu principaux, comme dans *Outils informatique II*. Les annexes, images, données et documents de préparation peuvent rester dans leurs dossiers propres. `_book/`, `.quarto/` et les fichiers de rendu sont générés par Quarto.

## Qui contient quoi ?

| Fichier | Informations du cours | Réglages partagés |
|---|---|---|
| `_quarto.yml` | Titre, auteur, URL GitHub, chapitres, annexes, bibliographie, ressources propres au cours et noyau Python | Référence `_template.yml` avec `metadata-files` |
| `_template.yml` | Aucun titre, liste de chapitres ou nom de fichier BibTeX propre à un cours | Thèmes clair/sombre, CSS/JS, filtres, encadrés, navigation générique, langue et options de rendu |
| `slides/_quarto.yml` | Auteur, bibliographie et sélection des présentations | Référence le `_template.yml` situé dans `slides/` |
| `slides/_template.yml` | Aucun titre de cours ni nom de fichier BibTeX | Format clean-revealjs, animations, plugins, mise en page, ressources et filtres |

Chaque `_quarto.yml` utilise :

```yaml
metadata-files:
  - _template.yml
```

Les réglages propres au cours peuvent surcharger les valeurs du modèle. Une adaptation valable pour un seul cours doit rester dans son `_quarto.yml` ou dans le document concerné, afin que les fichiers `_template.yml` restent partageables.

Le sous-projet `slides/` déclare explicitement `project: type: default` pour charger sa configuration et ses métadonnées. Le livre conserve `project: type: book`.

## Bibliographie : un nom par cours

Tous les fichiers BibTeX sont placés dans **`assets/`**, mais leur nom n’est pas imposé par le modèle.

Exemples actuels :

- *Analyse géospatiale* : `assets/geospatial.bib`.
- *Outils informatique II* : `assets/OI2.bib`.

Le livre déclare ce chemin dans son `_quarto.yml`. Les slides déclarent le chemin correspondant, par exemple `../assets/geospatial.bib`, dans leur propre `_quarto.yml`. Aucun fichier `_template.yml` ne contient de clé `bibliography`.

Dans le squelette du modèle, `assets/references.bib` est seulement un exemple à renommer lors de la création d’un cours. Il ne faut jamais écraser la bibliographie d’un cours lors d’une mise à jour du modèle.

Les bibliographies synchronisées avec Zotero sont gérées par Zotero, sans modification manuelle des entrées. Lorsqu’une référence doit être ajoutée, fournir son BibTeX dans la conversation pour import dans Zotero.

## Échanges du modèle vers un cours

### Nouveau cours

Copier le squelette du modèle, puis personnaliser les deux `_quarto.yml` : titre, organisation des chapitres, bibliographie, auteurs et URL du dépôt. Ajouter les contenus dans `course/` et `slides/`.

### Mise à jour d’un cours existant

1. Comparer et copier les fichiers `_template.yml` du livre et des slides.
2. Copier les fichiers de style, scripts, filtres ou extensions nécessaires à la nouvelle fonctionnalité.
3. **Conserver les `_quarto.yml` locaux**, les bibliographies, données et contenus.
4. Examiner le diff Git, rendre un chapitre et une présentation, puis committer la mise à jour.

Un nouveau plugin demande souvent une modification YAML **et** l’ajout de son dossier dans `_extensions/`. Copier seulement la ligne YAML ne suffit pas.

## Échanges d’un cours vers le modèle

Si l’on améliore une fonctionnalité dans un cours, modifier les fichiers partageables correspondants : `_template.yml`, styles, filtres, scripts ou extensions. Les titres, noms BibTeX et autres informations locales étant dans les `_quarto.yml`, ils n’ont pas à remonter vers le modèle.

1. Vérifier que le changement est réutilisable et non spécifique au cours.
2. Examiner le diff, par exemple :

   ```sh
   git diff -- _template.yml slides/_template.yml
   ```

3. Reporter les fichiers ou les changements pertinents dans le dépôt du modèle, avec leurs dépendances.
4. Examiner et committer le diff dans ce dépôt.
5. Propager ensuite cette amélioration vers les autres cours qui en ont besoin.

`git add -p` permet de sélectionner les portions d’un diff à committer si plusieurs changements ont été mélangés. La séparation des responsabilités dans les YAML évite surtout d’avoir à deviner quelles lignes sont locales et quelles lignes sont génériques.

Ce flux fonctionne **dans les deux sens**, mais ne constitue pas une synchronisation automatique. Git assure l’historique, la revue et les fusions ; les fichiers sont transférés explicitement entre les dépôts. Aucun `push` GitHub n’est exécuté par les scripts de construction.

## Noms des fichiers

| Élément | Convention |
|---|---|
| Chapitre | `course/class_01.qmd` |
| Présentation | `slides/slides_class_01.qmd` |
| Notebook | `course/class_01.ipynb` |

Utiliser deux chiffres et le même numéro pour les trois supports. Les titres affichés peuvent contenir espaces et accents ; les noms des fichiers sources évitent ces caractères.

Les noms historiques `course/semaine_04.qmd` et `slides/slides_semaine_04.qmd` restent pris en charge. Les scripts ne nécessitent pas de renommer les fichiers existants de *Outils informatique II*.

## Construction, comme dans Outils informatique II

Les scripts sont des fichiers locaux ordinaires et trouvent le projet relativement à leur emplacement. Ils sont portables entre les cours et ne dépendent pas du dossier central.

Avec l’environnement Python adapté actif, depuis le dossier d’un cours :

```sh
# Livre et profils existants
quarto preview
quarto render --profile answer
quarto render --profile question

# Une présentation, sans exécuter les cellules
quarto render slides/slides_class_04.qmd --no-execute

# Présentations et notebooks : sélecteurs numériques ou noms de fichiers
python scripts/render_slides.py 4 --no-pdf
python scripts/render_notebooks.py 4

# Flux de construction existant : slides, notebooks, puis livre
python scripts/render_all.py --no-pdf
```

Les scripts de rendu ne synchronisent pas les modèles. `render_all.py` conserve le fonctionnement de *Outils informatique II*, notamment sa question finale de publication : il ne faut confirmer cette publication que si elle est souhaitée. La génération PDF requiert une installation existante de Decktape et, pour la compression, Ghostscript ; `--no-pdf` l’évite.

La première classe, sans pratique, est exclue de la génération des notebooks. `quarto convert` produit des notebooks non exécutés ; les profils du livre ne filtrent pas leur contenu source.

## Un seul livre, les profils existants

Les fichiers `_quarto-answer.yml` et `_quarto-question.yml` sont repris de *Outils informatique II*. On ne crée pas de livres enseignant et étudiant distincts. Le même projet est rendu avec le profil choisi.

Les réponses rédigées peuvent utiliser `.content-visible when-meta="answers"`. Les surcharges d’un document restent prioritaires selon les règles Quarto.

## GitHub et autonomie

Commiter les configurations, styles, filtres, extensions et scripts avec les sources du cours. Ne pas ignorer les dossiers `_extensions/` requis au rendu. Un clone du cours contient alors le nécessaire pour son modèle, sans dossier central, sans gestionnaire Python et sans récupération spéciale de sous-projet Git.

Quarto, les dépendances Python et les données requises restent à installer ou fournir. Les ressources web et les services GEE peuvent nécessiter Internet. Aucun dépôt distant, submodule ou subtree n’est configuré par cette mise en place.

## Documentation technique

- Métadonnées partagées Quarto : https://quarto.org/docs/projects/quarto-projects.html
- Extensions et suivi dans Git : https://quarto.org/docs/extensions/managing.html

## Présentations extractibles comme projet autonome

Le dossier `slides/` peut être copié seul : il contient ses YAML, `_extensions/`, assets, CSL et copies locales des bibliographies. Les données et styles utilisés par le code doivent également y être présents, avec des chemins internes au dossier.

Les bibliographies ont un nom propre à chaque cours, y compris dans `slides/assets/`. Le script `render_slides.py` rafraîchit ces copies depuis les exports du dossier `assets/` du cours avant le rendu. Après une mise à jour Zotero, utiliser ce script pour rafraîchir la copie avant extraction ; un `quarto preview` direct utilise la copie locale déjà présente. Pour un talk autonome, exporter directement sa bibliographie dans son propre `assets/`.

Depuis le dossier extrait, `quarto preview` fonctionne sans le dépôt du cours. Il faut copier **tout le dossier**, notamment `assets/`, `data/`, `img/` et `_extensions/` requis ; le seul fichier QMD ne suffit pas.

Les liens vers les pages du cours restent des liens de lecture : ils ne sont pas requis pour construire le deck. Pour publier le deck à une autre adresse, adapter ces liens vers les pages publiées du cours si nécessaire.

## Icônes des profils sur la diapositive de titre

Dans `slides/_quarto.yml`, le bloc optionnel `author-links` définit `researchgate`, `github`, `scholar` et `website` avec leurs URL complètes. Les icônes apparaissent après l’ORCID du premier auteur ; seuls les liens renseignés sont affichés. L’ORCID reste défini dans les métadonnées normales de l’auteur. Le modèle générique conserve des exemples commentés à compléter.

La fonctionnalité partageable est le filtre `course/author-links`, déclaré dans `slides/_template.yml`, accompagné de `slides/_extensions/course/author-links/`. Les URL personnelles restent dans `_quarto.yml`. Le filtre utilise Font Awesome, déjà chargé par le thème des présentations. Lors d’un transfert du modèle, copier la déclaration et le dossier d’extension ensemble. Le dossier `slides/` reste autonome.

## Documentation du modèle

[Consulter la documentation](https://e5k.github.io/_quarto-teaching-template/) · [Dépôt GitHub](https://github.com/e5k/_quarto-teaching-template)

Le site de documentation se trouve dans [doc/index.qmd](doc/index.qmd). Il contient quatre guides : prise en main, livre, présentations et maintenance, avec les fonctionnalités locales, des exemples et le flux Git dans les deux sens.

Depuis le dossier `doc/`, lancer `quarto preview` pour le consulter ou `quarto render` pour reconstruire le site dans `doc/_site/`. Le projet de documentation est indépendant du livre du cours. Les exemples de présentations pré-rendus restent dans `doc/assets/demos/slides/` et doivent être régénérés si le thème change.


### Publication sur GitHub Pages

Le dépôt public est https://github.com/e5k/_quarto-teaching-template et la documentation est publiée à https://e5k.github.io/_quarto-teaching-template/. Le workflow `.github/workflows/publish-docs.yml` reconstruit uniquement le projet `doc/` après un push qui modifie ce dossier sur `main`. Il met à jour la branche `gh-pages`, puis déploie le même site avec GitHub Pages. Le workflow peut aussi être lancé manuellement depuis Actions. Les fichiers générés `doc/_site/` restent exclus de `main`.

Pour publier manuellement une documentation déjà rendue : `quarto publish gh-pages doc --no-render --no-browser`. Pour inclure le rendu, retirer `--no-render`.
