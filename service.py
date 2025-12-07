import os
import time
from typing import Any, Dict, Optional
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from icecream import ic
import snoop
from dotenv import load_dotenv


load_dotenv()



class ChatRequest(BaseModel):
    query: str


class ChatResponse(BaseModel):
    query: str
    answer: str
    response_time: float


class ChatService:
    """
    ChatService wraps LLM client initialization, prompt handling, and query calls.
    """
    
    # @snoop
    def __init__(
        self,
        query: str = None,
        model_name: str = "llama-3.3-70b-versatile",
        temperature: float = 0.2,
        prompt_template: Optional[Any] = None,
    ):
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        
        if not self.groq_api_key:
            raise RuntimeError("GROQ_API_KEY is not set")

        self.model_name = model_name
        self.temperature = temperature
        self.query = query  # Store query for auto-use

        # Initialize the LLM client
        self.llm = self._init_client()

        # Initialize the prompt template
        if prompt_template is not None:
            self.prompt = prompt_template
        else:
            self.prompt = self._default_prompt_template()

    def _init_client(self) -> Any:
        """Initialize and return the LLM client instance."""
        try:
            llm = ChatGroq(
                model_name=self.model_name,
                temperature=self.temperature,
                groq_api_key=self.groq_api_key,
            )
            ic("LLM client initialized")
            return llm
        except Exception as e:
            ic("Failed to initialize LLM client")
            raise

    def _default_prompt_template(self) -> Any:
        """Create and return the default prompt template."""
        try:
            return ChatPromptTemplate.from_template(
                """
You are a helpful, intelligent, and friendly AI assistant.

Answer the user's questions clearly, naturally, and conversationally.
Use simple and easy-to-understand language.
If the user asks for explanations, provide them step-by-step.
If the user asks for opinions or general knowledge, respond like a normal chat assistant.

User Question: {input}
"""
            )
        except Exception as e:
            ic("Failed to build default prompt template")
            raise

    def _build_prompt(self, user_query: str) -> str:
        """Format and return the final prompt string for the LLM."""
        try:
            return self.prompt.format(input=user_query)
        except Exception:
            try:
                return str(self.prompt).format(input=user_query)
            except Exception as e:
                ic("Failed to build prompt")
                raise RuntimeError("Prompt formatting failed") from e

    def query_chat(self, query: Optional[str] = None) -> Dict[str, Any]:
        """
        Synchronous method that sends a query to the LLM and returns a dict with the normalized answer.
        If query is not provided, uses the query from __init__.
        """
        # Use provided query or fall back to the one from __init__
        final_query = query if query is not None else self.query
        
        if not final_query or not final_query.strip():
            raise ValueError("query must be a non-empty string")

        final_prompt = self._build_prompt(final_query)

        start = time.time()
        try:
            raw_response = self.llm.invoke(final_prompt)
        except Exception as e:
            ic("LLM invocation failed")
            raise RuntimeError(f"LLM invocation failed: {e}") from e
        elapsed = time.time() - start

        answer = raw_response.content
        return {"query": final_query, "answer": answer, "response_time": elapsed}


# Example usage
if __name__ == "__main__":
    # Option 1: Pass query in __init__ and call query_chat() without arguments
    chat_service = ChatService(query="Who is Merab Dvalishvili a champion?")
    result = chat_service.query_chat()  # Uses query from __init__
    print(result["answer"])
    
    # Option 2: Override the init query by passing a new query to query_chat()
    # chat_service = ChatService()

    # result2 = chat_service.query_chat(" Merab Dvalishvili is UFC fighter stupid?")  # Uses new query
    # ic(result2)