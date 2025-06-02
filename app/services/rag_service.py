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
            embedding_function=embeddings,

        )

        llm = ChatPerplexity(
            model="sonar-pro",
            temperature=0.7,
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

        Regras:
        1. Se o contexto for irrelevante, responda "Não consta na base"
        2. Priorize informações de PRINCIPIO_ATIVO e CLASSE_TERAPEUTICA
        3. Formate respostas com marcadores
        """
        
        return RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vector_store.as_retriever(
                search_kwargs={"k": 10}  
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
    
    print("\nDocumentos Recuperados:")
    for idx, doc in enumerate(result["source_documents"][:5], 1):
        print(f"\nDocumento {idx}:")
        print(f"Fonte: {doc.metadata['source']}")
        print(f"Classe Terapêutica: {doc.metadata.get('CLASSE_TERAPEUTICA', 'N/A')}")
        print(f"Conteúdo: {doc.page_content[:500]}...")
    
    sources = [{
        "content": doc.page_content,
        "source": doc.metadata.get('source', 'Desconhecido'),
        "page": doc.metadata.get('page', 'N/A')
    } for doc in result["source_documents"]]
    
    return result["result"], sources