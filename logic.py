import os
import time
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders.text import TextLoader
from langchain_community.document_loaders import PyPDFDirectoryLoader
from dotenv import load_dotenv
from icecream import ic

# Load environment variables
load_dotenv()

# Manually set the API keys
groq_api_key = os.getenv("GROQ_API_KEY")


# Initialize the model
llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    temperature=0.2,
    groq_api_key=groq_api_key
)

# Define the prompt template for generating responses
prompt = ChatPromptTemplate.from_template(
    """
    You are a helpful, intelligent, and friendly AI assistant.

Answer the user's questions clearly, naturally, and conversationally.
Use simple and easy-to-understand language.
If the user asks for explanations, provide them step-by-step.
If the user asks for opinions or general knowledge, respond like a normal chat assistant.

User Question: {input}
    """
)

def query_chat(query: str, llm, prompt):
    try:
        # Prepare the final prompt with the template
        final_prompt = prompt.format(input=query)

        # Time the response
        start = time.process_time()
        response = llm.invoke(final_prompt)
        elapsed = time.process_time() - start

        return {
            "query": query,
            "answer": response,
            "response_time": elapsed
        }

    except Exception as e:
        return {"error": str(e)}



a = query_chat(query = "Are u working fine?", llm=llm, prompt=prompt)

ic(a["answer"].content)

