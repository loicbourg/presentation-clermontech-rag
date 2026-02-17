---
layout: cover
#  Photo de <a href="https://unsplash.com/fr/@daria_kraplak?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Daria Kraplak</a> sur <a href="https://unsplash.com/fr/photos/black-typewriter-d34DtRp1bqo?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>
background: /img/cover.jpg
theme: seriph
#backgroundSize: contain
title: Faites parler vos données avec le RAG
# slide transition: https://sli.dev/guide/animations.html#slide-transitions
transition: slide-left
# enable MDC Syntax: https://sli.dev/features/mdc
mdc: true
# take snapshot for each slide in the overview
overviewSnapshots: true
colorSchema: light
lineNumbers: true
---

# Faites parler vos données avec le RAG

---
layout: center
---

# Loïc BOURG

Lead technique @ITNetwork

---
layout: center
---

# RAG ?

**R**etrieval **A**ugmented **G**eneration

<v-clicks>

- Ancrer les réponses sur des faits réels
- Actualiser les connaissances en temps réel
- Citer les sources utilisées

</v-clicks>


---
layout: default
---



```mermaid
graph LR
    U[Utilisateur] -- "1. Question" --> S[Backend RAG]
    S -- "2. Recherche vectorielle" --> D[(BDD vectorielle)]
    D -- "3. Documents pertinents" --> S
    S -- "4. Contexte + question" --> L[LLM]
    L -- "5. Réponse (avec citations)" --> S
    S -- "6. Réponse" --> U
 
```

---
layout: center
---

# Le contexte du projet

<v-clicks>

- Chaîne d'hôtels d'environ 10 hôtels en France souhaitant grossir
- Besoin d'augmenter l'autonomie des nouveaux arrivants.
- Beaucoup de documentation mais dans différentes applications

</v-clicks>

---
layout: default
---

# Recherche vectorielle
Quand est-ce que je dois sortir les poubelles à l'hôtel opéra ?

---
layout: center
---

# Indexation des documents dans la base vectorielle

<v-clicks>

- Découpage des longs documents en petits morceaux ("chunks")
- Ajout de métadonnées à l'intérieur des chunks
- Génération des embeddings des chunks
- Insertion

</v-clicks>

---
layout: center
---

# Embedding ?

<v-clicks>

- Transformation de texte en un vecteur représentant son contenu sémantique
- Des textes proches en sens ont des vecteurs proches

</v-clicks>

---
layout: default
---

```python {1-7|1-3,9-10|1-3,12-18}
A = "procédure de check-in"
B = "enregistrement à la réception"
C = "recette de pancakes"

vec_A = compute_embedding(A)
vec_B = compute_embedding(B)
vec_C = compute_embedding(C)

sim_AB = cosine_similarity(vec_A, vec_B)
sim_AC = cosine_similarity(vec_A, vec_C)

print("sim(A, B) =", sim_AB)  # -> 0.999 
print("sim(A, C) =", sim_AC)  # -> 0.293 

```

---
layout: default
---

# Recherche vectorielle
Quand est-ce que je dois sortir les poubelles à l'hôtel opéra ?

<div class="flex items-center justify-center h-60">
<div class="text-left">
<v-clicks>

- Embedding de la question
- Recherche des "chunks" les plus proches au niveau sémantique de la question

</v-clicks>
</div>
</div>

---
layout: default
---

```python
query_vector = compute_embedding(question)

top_k = 5
matches = vector_db.search(vector=query_vector, top_k=top_k)

chunks = [m.payload["text"] for m in matches]
```


---
layout: default
---


```md
---
titre: "Hôtel opéra: les informations de base"
auteur: "Service Exploitation"
lien: "https://www.doc-interne.com/korner-opera/informations-generales"
---

…

## Horaires de passage des poubelles
Poubelle verte/grise : Tous les jours à 16h devant l'hôtel.
Poubelle jaune : Lundi, mercredi et vendredi à 16h devant l'hôtel.
Conteneur à verre : Derrière le bâtiment en face de l'hôtel.

…
````



---
layout: default
---

# Génération de la réponse
Quand est-ce que je dois sortir les poubelles à l'hôtel opéra ?


<div class="flex items-center justify-center h-60 text-center">

<div class="flex items-center justify-center h-60">
<div class="text-left">
<v-clicks>

- On envoie le prompt système et les chunks au LLM
- On renvoie la réponse à l'utilisateur

</v-clicks>
</div>
</div>

</div>

---
layout: default
---


```python {1-7|10-13|15}
SYSTEM_PROMPT = """
Tu es un assistant RAG.
Règles :
- Réponds uniquement à partir des CHUNKS fournis. N’invente rien.
- Si l’info n’est pas dans les CHUNKS, dis "Je ne sais pas".
- À la fin, ajoute une section "Sources" avec des liens Markdown.
Format attendu : - [Titre du chunk](source_url) (ou [Chunk <id>](source_url) si le titre est absent)
"""

messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": f"Question: {question}\n\nCHUNKS:\n{context}"},
]

response = LLM.generate(messages=messages, temperature=0.1)
```


---
layout: default
---

```markdown
Les poubelles à l'Hôtel Opéra doivent être sorties selon le calendrier suivant :

Poubelle verte/grise : Tous les jours à 16h devant l'hôtel.
Poubelle jaune : Lundi, mercredi et vendredi à 16h devant l'hôtel.
Conteneur à verre : Derrière le bâtiment en face de l'hôtel.

## Sources
- [Hôtel opéra: les informations de base](https://www.doc-interne.com/opera/informations-generales)

```

---
layout: two-cols-header
---

# Et si ça répond mal ?

::left::

<v-click>

## Si le bon chunk n'est pas retourné

</v-click>
<v-clicks>

- Jouer sur le nombre de chunks récupérés
- Augmenter la question avec un glossaire pour le jargon interne
- Passer en recherche hybride (vectoriel + textuel)
- Ajouter un reranker
- Ajouter du filtrage par métadonnées
- Réduire le nombre de chunks en base
- ...

</v-clicks>

::right::

<v-click>

## Si la réponse n'est pas bonne

</v-click>

<v-clicks>

- Réduire le nombre de chunk récupéré (top K)
- Changer de modèle
- Modifier le prompt système
- ...

</v-clicks>


<style>
.two-cols-header {
  column-gap: 20px; /* Adjust the gap size as needed */
}
</style>

---
layout: center
---

# Conclusion


---
layout: center
---

# Questions ?