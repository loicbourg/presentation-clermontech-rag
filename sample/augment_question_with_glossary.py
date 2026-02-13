from langchain.schema.runnable.config import RunnableConfig
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

from src.llms.system_prompt import SYSTEM_PROMPT_MESSAGE

GET_AUGMENTED_QUESTION_NAME = "augmented_question"
GET_AUGMENTED_QUESTION_FIELD = "question_augmentée"

GET_AUGMENTED_QUESTION_SCHEMA = {
    "type": "function",
    "function": {
        "name": GET_AUGMENTED_QUESTION_NAME,
        "description": "Ajoute les définitions du lexique à la phrase ou question donnée",
        "parameters": {
            "type": "object",
            "properties": {
                GET_AUGMENTED_QUESTION_FIELD: {
                    "type": "string",
                    "description": "La phrase ou question augmentée",
                },
            },
            "required": [GET_AUGMENTED_QUESTION_FIELD],
        },
    },
}


def build_prompt_to_augment_question_with_glossary(glossary: str, question: str) -> str:
    """Builds prompt to augment question with glossary."""
    return (
        "Détecte les mots contenus dans le lexique et renvoie la même question ou phrase avec"
        " la définition des mots entre parenthèse (acronyme: définition)."
        'Par exemple : "Où est HKO ?" devient "Où est HKO (HKO: Hôtel Korner Opéra) ?"'
        'Par exemple : "Où est l\'hôtel Korner Opéra ?" devient "Où est l\'hôtel Korner Opéra'
        ' (HKO: Hôtel Korner Opéra) ?"'
        'Par exemple : "Où est opéra ?" devient "Où est l\'hôtel Korner Opéra'
        ' (HKO: Hôtel Korner Opéra) ?"'
        "S'il n'y a pas de définitions à ajouter, renvoie la phrase telle quelle."
        + f"""
    =======
    LEXIQUE : \n\n {glossary}
    =======
    QUESTION : {question}
    """
    )


def get_augmented_question_with_glossary(
    question: str,
    glossary: str,
    llm: ChatOpenAI,
    langchain_config: RunnableConfig | None = None,
) -> str:
    """Get a single question from the conversation history and the user input."""
    prompt = build_prompt_to_augment_question_with_glossary(
        glossary=glossary,
        question=question,
    )

    response = llm.invoke(
        input=[SYSTEM_PROMPT_MESSAGE, HumanMessage(content=prompt)],
        tools=[GET_AUGMENTED_QUESTION_SCHEMA],
        config=langchain_config,
    )

    return response.tool_calls[0]["args"][GET_AUGMENTED_QUESTION_FIELD]  # type: ignore