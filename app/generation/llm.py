from langchain_google_genai import ChatGoogleGenerativeAI

from app.config import GOOGLE_API_KEY


def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=GOOGLE_API_KEY,
        temperature=0,
    )


def generate_answer(prompt: str) -> str:
    llm = get_llm()

    response = llm.invoke(prompt)

    return response.content