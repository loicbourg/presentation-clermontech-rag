# Plan retravaille - "Faites parler vos donnees avec le RAG"

## Objectif
Proposer un talk de 10 minutes plus coherent avec le titre et la description:
- focus sur la fiabilite des reponses grace au RAG;
- retour d'experience concret (assistant interne pour une chaine d'hotels);
- parcours complet d'une question, sans digressions techniques.

## Contraintes de format
- 10 min de talk + 5 min de questions.
- 9 a 10 slides maximum.
- Peu de texte par slide.
- 2 schemas maximum.
- 1 extrait de code court maximum (avec highlights progressifs).

## Message cle a faire retenir
Un RAG fiable n'est pas un "prompt magique": c'est une chaine simple de decisions
(reformuler, router, filtrer, retrouver, evaluer) qui transforme des documents internes en reponses utiles.

## Fil rouge (question unique)
Question utilisateur:
"Quand est-ce que je dois sortir les poubelles a HKO ?"

Cette question sert a montrer toutes les etapes:
- ambiguite metier (acronyme HKO);
- choix des bonnes sources;
- recherche des bons passages;
- reponse finale avec source citee.

## Hors scope (pour rester dans les 10 min)
- Pas de deep dive mathematique sur les embeddings.
- Pas de comparatif de vector DB ou de modeles d'embedding.
- Pas de detail d'implementation LangChain par composant.
- Pas de focus "agentic RAG" (a garder pour les questions).

## Plan minute par minute

### 1) 0:00 -> 0:45 | Slide 1 - Titre + promesse
Contenu:
- "Les LLM repondent vite, mais pas toujours juste."
- Promesse: "En 10 minutes, je vous montre comment rendre les reponses plus fiables avec un RAG."

Intention:
- Poser le probleme immediatement.
- Annoncer un plan simple et concret.

### 2) 0:45 -> 1:45 | Slide 2 - Contexte metier
Contenu:
- Chaine d'hotels (environ 10 etablissements).
- Documentation de qualite, mais dispersee et peu exploitee.
- Besoin: accelerer l'autonomie des nouveaux arrivants.

Intention:
- Montrer un besoin operationnel reel, pas un POC abstrait.

### 3) 1:45 -> 2:30 | Slide 3 - Le schema global en 5 etapes
Contenu:
- Schema unique du pipeline:
1. Reformulation
2. Routage des sources
3. Filtrage metadonnees
4. Recherche vectorielle + selection
5. Generation + suivi qualite

Intention:
- Donner la carte mentale du reste du talk.

### 4) 2:30 -> 3:30 | Slide 4 - Etape 1: reformulation de la demande
Contenu:
- Exemple avant/apres avec HKO -> Hotel Korner Montmartre.
- Role du glossaire metier + historique de conversation.

Intention:
- Faire comprendre que la qualite commence avant la recherche.

### 5) 3:30 -> 4:30 | Slide 5 - Etape 2: routage des familles de sources
Contenu:
- Exemple de familles: conciergerie, chambres, maintenance, fournisseurs.
- Pourquoi: eviter le bruit et ne pas noyer les petites sources.

Intention:
- Expliquer simplement la reduction du champ de recherche.

### 6) 4:30 -> 5:30 | Slide 6 - Etape 3: extraction de filtres metadonnees
Contenu:
- Filtres extraits de la question: hotel, service, categorie.
- Prefiltrage des documents/chunks avant la recherche vectorielle.

Intention:
- Montrer un levier concret de precision.

### 7) 5:30 -> 6:45 | Slide 7 - Etape 4: recherche vectorielle + generation
Contenu:
- Recherche des passages les plus pertinents.
- Envoi au modele: question reformulee + passages + prompt systeme.
- Reponse attendue: concise, actionnable, source citee.

Intention:
- Boucler le parcours "de la question a la reponse".

Note visuelle:
- Ici, possible extrait de code unique (10-15 lignes max) montrant la pipeline.

### 8) 6:45 -> 8:15 | Slide 8 - Etape 5: suivi qualite et debug
Contenu:
- Dataset de questions/reponses attendues.
- Retours utilisateurs.
- Mini grille de diagnostic:
1. Mauvais chunks trouves -> agir sur retrieval (BM25 hybride, reranker, filtres).
2. Bons chunks mais mauvaise reponse -> agir sur prompts et contexte.

Intention:
- Montrer la demarche d'amelioration continue.

### 9) 8:15 -> 9:15 | Slide 9 - Resultats et limites
Contenu:
- Ce qui a marche: acces plus rapide a l'info, meilleur onboarding.
- Limites: qualite source, couverture de cas, maintenance continue.

Intention:
- Rester honnete et credible.

### 10) 9:15 -> 10:00 | Slide 10 - Conclusion + ouverture
Contenu:
- Recap en une phrase:
"La fiabilite d'un RAG vient du pipeline, pas d'une seule brique."
- Transition vers Q&A.

Intention:
- Finir net, laisser du temps aux questions.

## Materiaux a preparer avant les slides
- 1 schema principal du pipeline (utilisable sur plusieurs slides).
- 1 exemple fil rouge complet (question -> reponse + source).
- 1 extrait de code tres court (pipeline), avec highlights.
- 1 slide "grille de debug" avec 2 cas uniquement.

## Checklist anti-derapage (important)
- Chaque slide doit tenir en 45-75 secondes.
- Si une slide demande plus de 90 secondes: couper.
- Maximum 1 idee forte par slide.
- Supprimer tout element non relie au fil rouge.
- Garder "agentic RAG" et comparatifs techniques pour la session Q&A.
