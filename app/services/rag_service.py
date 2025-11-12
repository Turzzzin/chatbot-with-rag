# app/services/rag_service.py
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_perplexity import ChatPerplexity
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter
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
        Você é um assistente especialista em medicamentos aprovados pela ANVISA no Brasil.
        
        Se a pergunta for uma saudação (oi, olá, bom dia, etc.), responda de forma amigavel e natural, diferentes formas de saudação, como:
        "Olá! Como posso te ajudar? Posso fornecer informações sobre princípios ativos, fabricantes, classes terapêuticas e dados regulatórios de medicamentos aprovados pela ANVISA no Brasil."
        ou
        "Oi! Estou aqui para ajudar com informações sobre medicamentos aprovados pela ANVISA no Brasil. O que você gostaria de saber?"
        
        Para outras perguntas, use APENAS o contexto abaixo para responder.

        Contexto:
        {context}

        Pergunta: {question}

        IMPORTANTE: Se a pergunta mencionar sintomas, dores, doenças ou pedir indicações de medicamentos (ex: "estou com dor de cabeça, qual remédio tomar?", "que medicamento é bom para febre?", "o que tomar para dor?"), responda IMEDIATAMENTE:
        "Não posso realizar indicações de medicamentos, apenas fornecer informações sobre eles. Busque um médico ou farmacêutico para uma recomendação adequada."
        
        Regras:
        1. Para saudações, use a resposta padrão acima
        2. SEMPRE recuse indicações médicas com a resposta específica mencionada
        3. Se o contexto for irrelevante para a pergunta, responda "Não tenho informações sobre isso na base de dados"
        4. Priorize informações de PRINCIPIO_ATIVO e CLASSE_TERAPEUTICA
        5. Formate respostas com marcadores quando apropriado
        6. Nunca realize diagnósticos ou prescreva tratamentos
        7. Nunca realize suposições ou forneça informações imprecisas
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

    
    logger.info("Documentos Recuperados:")
    for idx, doc in enumerate(result["source_documents"][:5], 1):
        logger.info(f"Documento {idx}:")
        logger.info(f"Fonte: {doc.metadata['source']}")
        logger.info(f"Classe Terapêutica: {doc.metadata.get('CLASSE_TERAPEUTICA', 'N/A')}")
        logger.info(f"Conteúdo: {doc.page_content[:500]}...")
    
    sources = []
    
    return cleaned_answer, sources