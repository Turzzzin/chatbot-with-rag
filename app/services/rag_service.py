# app/services/rag_service.py
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_perplexity import ChatPerplexity
from langchain_core.prompts import PromptTemplate
from app.utils.config import settings
from fastapi import Request
import logging

logger = logging.getLogger(__name__)

def initialize_rag():
    try:

        embeddings = SentenceTransformerEmbeddings(
            model_name=settings.EMBEDDINGS_MODEL
        )

        vector_store = Chroma(
            persist_directory=settings.CHROMA_DB_PATH,
            embedding_function=embeddings
        )

        llm = ChatPerplexity(
            model="sonar-pro",
            temperature=0.3,
            max_tokens=512,
            api_key=settings.PPLX_API_KEY
        )
        
        prompt_template = """
        Você é um assistente médico especialista em medicamentos. 
        Use APENAS o contexto abaixo para responder. 
        Se não souber a resposta, diga 'Não tenho informações suficientes'.

        Contexto:
        {context}

        Pergunta: {question}

        Resposta concisa e técnica:
        """
        
        return RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vector_store.as_retriever(
                search_kwargs={"k": 5}  
            ),
            return_source_documents=True,
            chain_type_kwargs={
                "prompt": PromptTemplate(
                    template=prompt_template,
                    input_variables=["context", "question"]
                )
            }
        )
    
    except Exception as e:
        logger.error(f"Erro ao inicializar RAG: {str(e)}")
        raise

async def get_rag_response(question: str, request: Request):  
    chain = request.app.state.rag_chain 
    result = chain.invoke({"query": question})
    
    sources = [{
        "source": doc.metadata.get('source', 'Desconhecido'),
        "page": doc.metadata.get('page', 'N/A')
    } for doc in result["source_documents"]]
    
    return result["result"], sources