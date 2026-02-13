from collections.abc import AsyncIterable
from typing import cast

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

from src.constants import (
    CITE_SOURCE_PROMPT,
    PROMPT_RESPONSE_WHEN_RETRIEVED_CHUNKS_ARE_NOT_RELEVANT,
    TICKET_MAINTENANCE_NAME,
)
from src.llms.system_prompt import SYSTEM_PROMPT_MESSAGE


def build_prompt_with_question_chunks_and_history(
    question: str,
    chunk_contents: list[str],
    message_history_concatenated: str = "",
    relevant_sources: list[str] | None = None,
) -> str:
    """Merge the chunks contents, history and question to build the full prompt."""
    if relevant_sources is None:
        relevant_sources = []
    PROMPT_BEFORE_DOCUMENT = ""
    if len(relevant_sources) == 1 and relevant_sources[0] == TICKET_MAINTENANCE_NAME:
        PROMPT_BEFORE_DOCUMENT = """**INSTRUCTIONS IMPÉRATIVES POUR LE TRAITEMENT DES TICKETS :**

1.  **RÈGLE ABSOLUE N°1 - NE JAMAIS OMETTRE DE TICKETS DISTINCTS MÊME S'ILS SONT SIMILAIRES :**
    *   Tu dois examiner **CHAQUE** document de ticket fourni, un par un, sans exception.
    *   Si un ticket correspond aux critères de la question (hôtel, 'Statut affiché pour l'utilisateur', etc.), il **DOIT IMPÉRATIVEMENT** être inclus dans ta réponse.
    *   **NE JAMAIS, JAMAIS OMETTRE UN TICKET PERTINENT SOUS PRÉTEXTE QU'IL RESSEMBLE À UN AUTRE.**
    *   Même si deux (ou plus) tickets ont le même titre, le même détail, le même auteur, ou d'autres champs identiques : s'ils possèdent des `Identifiants` différents, ils sont considérés comme des entrées **TOTALEMENT DISTINCTES** et **DOIVENT TOUS ÊTRE PRÉSENTÉS** dans la réponse.
    *   **Exemple critique :** Si tu trouves deux tickets concernant "YALA" pour une vérification, l'un avec l'`Identifiant: 4500` et l'autre avec l'`Identifiant: 4501`, tu **DOIS** lister ces DEUX tickets séparément. Ne pas le faire est une erreur. Cette instruction est **NON NÉGOCIABLE ET PRIORITAIRE SUR TOUTE AUTRE TENDANCE À LA SYNTHÈSE OU À LA DÉDUPLICATION**.

2.  **STATUT DU TICKET :** Pour déterminer si un ticket doit être référencé en réponse à une question sur son statut, tu dois **UNIQUEMENT** considérer la valeur du champ 'Statut affiché pour l'utilisateur'.

3.  **INTERVENTIONS :** Ignore le statut de l'intervention associée, sauf si la question porte explicitement sur les interventions.

4.  **IDENTIFIANT DANS LA RÉPONSE :** N'indique pas l'identifiant du ticket dans ta réponse sauf si l'utilisateur le demande explicitement.
"""

    history_section_in_prompt = (
        f"""=======
HISTORY: {message_history_concatenated}"""
        if len(message_history_concatenated) > 0
        else ""
    )

    return (
        "Étant donné les documents donnés ci-dessous et l'historique de la conversation, réponds à la question. "
        "Si tu ne trouves pas de réponse précise, essaye d'apporter à l'employé des informations utiles "
        "en rapport avec sa question à partir des documents. "
        "Si tu ne trouve strictement aucun élément de réponse dans les documents, "
        f"réponds avec cette phrase exacte : '{PROMPT_RESPONSE_WHEN_RETRIEVED_CHUNKS_ARE_NOT_RELEVANT}'. "
        "Ignore les documents qui ne semblent pas pertinents. "
        f"{CITE_SOURCE_PROMPT}"
        f"{PROMPT_BEFORE_DOCUMENT}"
        + (
            """
   =======
   DOCUMENTS :
   """
            + "".join(
                [
                    f"""-----
   \"\"\"
   {chunk_content}
   \"\"\"
   """
                    for chunk_content in chunk_contents
                ]
            )
            + f"""{history_section_in_prompt}
=======
QUESTION : {question}
=======
Si la question est une salutation, présente toi simplement.
"""
        )
    )


async def stream_answer_from_question_chunks_and_history(
    llm: ChatOpenAI,
    question: str,
    chunk_contents: list[str],
    message_history_concatenated: str,
    langchain_config: dict[str, list],
    relevant_sources: list[str],
) -> AsyncIterable[str]:
    """Stream the llm answer to the user question using relevant chunks and history."""
    prompt = build_prompt_with_question_chunks_and_history(
        question=question,
        chunk_contents=chunk_contents,
        message_history_concatenated=message_history_concatenated,
        relevant_sources=relevant_sources,
    )
    async for chunk in llm.astream(
        input=[SYSTEM_PROMPT_MESSAGE, HumanMessage(content=prompt)],
        config=langchain_config,  # type: ignore
    ):
        if chunk.content is not None:  # Check if content is not None
            yield cast(str, chunk.content)


def generate_answer_from_question_and_chunks(
    llm: ChatOpenAI,
    question: str,
    chunk_contents: list[str],
) -> tuple[str, str]:
    """Generate the llm answer to the user question using relevant chunks."""
    prompt = build_prompt_with_question_chunks_and_history(
        question=question,
        chunk_contents=chunk_contents,
    )
    return (
        llm.generate(messages=[[SYSTEM_PROMPT_MESSAGE, HumanMessage(content=prompt)]])
        .generations[0][0]
        .text
    ), prompt