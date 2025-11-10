# app/services/rag_service.py
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_perplexity import ChatPerplexity
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter  # <-- Adicionado
from app.utils.config import settings
from fastapi import Request
from app.utils.logger import logger
import re

def format_docs(docs):
    """Função auxiliar para formatar documentos recuperados em uma string única."""
    return "\n\n".join(doc.page_content for doc in docs)

def initialize_rag():
    try:
        logger.info("Inicializando RAG...")
        embeddings = HuggingFaceEmbeddings(
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
            api_key=settings.PPLX_API_KEY,
            timeout=60
        )
        
        retriever = vector_store.as_retriever(
            search_kwargs={"k": 20}
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
        4. Caso o usuário peça indicações de uso ou tratamento, responda "Não posso realizar indicações de uso ou tratamento." 
        5. Nunca realize diagnósticos ou prescreva tratamentos ou indique medicamentos
        6. Nunca realize suposições ou forneça informações imprecisas
        """
        
        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )

        setup_and_retrieval = RunnableParallel(
            context=itemgetter("query") | retriever,
            question=itemgetter("query")
        )

        answer_generation = (
            RunnablePassthrough.assign(context=lambda x: format_docs(x["context"]))
            | prompt
            | llm
            | StrOutputParser()
        )

        rag_chain = setup_and_retrieval | RunnableParallel(
            result=answer_generation,
            source_documents=itemgetter("context")
        )
        
        logger.info("RAG (LCEL) iniciado com sucesso!")
        return rag_chain
    
    except Exception as e:
        logger.error(f"Erro ao inicializar RAG: {str(e)}")
        raise

async def get_rag_response(question: str, request: Request):  
    chain = request.app.state.rag_chain 
    result = chain.invoke({"query": question})

    answer = result["result"]
    cleaned_answer = re.sub(r'\[\d+\]', '', answer)

    
    logger.info("\nDocumentos Recuperados:")
    for idx, doc in enumerate(result["source_documents"][:5], 1):
        logger.info(f"\nDocumento {idx}:")
        logger.info(f"Fonte: {doc.metadata['source']}")
        logger.info(f"Classe Terapêutica: {doc.metadata.get('CLASSE_TERAPEUTICA', 'N/A')}")
        logger.info(f"Conteúdo: {doc.page_content[:500]}...")
    
    sources = [{
        "content": doc.page_content,
        "source": doc.metadata.get('source', 'Desconhecido'),
        "page": doc.metadata.get('page', 'N/A')
    } for doc in result["source_documents"]]
    
    return cleaned_answer, sources