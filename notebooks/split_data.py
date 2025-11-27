import pandas as pd
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import os

# Desabilitar paralelismo e progresso
os.environ['TOKENIZERS_PARALLELISM'] = 'false'
os.environ['HF_HUB_DISABLE_PROGRESS_BARS'] = '1'

# ============================================
# 1. Configurar chave e modelo
# ============================================

#model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
model_name = "BAAI/bge-m3"

print("Carregando modelo de embeddings...")
embedding_function = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': True}
)
print("Modelo carregado!")

# ============================================
# 2. Carregar e limpar o dataset
# ============================================

df = pd.read_csv('DADOS_ABERTOS_MEDICAMENTOS.csv', sep=';', encoding='iso-8859-1')

print(f"Número de registros antes da limpeza: {len(df)}")

# ============================================
# 3. Converter linhas em textos semânticos
# ============================================

def row_to_text(row):
    return (
        f"TIPO DO PRODUTO: {row['TIPO_PRODUTO']}\n"
        f"NOME DO PRODUTO: {row['NOME_PRODUTO']}\n"
        f"PRINCÍPIO ATIVO: {row['PRINCIPIO_ATIVO']}\n"
        f"CLASSE TERAPÊUTICA: {row['CLASSE_TERAPEUTICA']}\n"
        f"CATEGORIA REGULATÓRIA: {row['CATEGORIA_REGULATORIA']}\n"
        f"EMPRESA DETENTORA DO REGISTRO: {row['EMPRESA_DETENTORA_REGISTRO']}\n"
        f"NÚMERO DO REGISTRO: {row['NUMERO_REGISTRO_PRODUTO']}\n"
        f"DATA DE FINALIZAÇÃO DO PROCESSO: {row['DATA_FINALIZACAO_PROCESSO']}\n"
        f"DATA DE VENCIMENTO DO REGISTRO: {row['DATA_VENCIMENTO_REGISTRO']}\n"
        f"SITUAÇÃO DO REGISTRO: {row['SITUACAO_REGISTRO']}\n"
        f"NÚMERO DO PROCESSO: {row['NUMERO_PROCESSO']}"
    )

documents = []
for _, row in df.iterrows():
    text = row_to_text(row)
    metadata = {
        "source": "DADOS_ABERTOS_MEDICAMENTOS",
        "NOME_PRODUTO": str(row["NOME_PRODUTO"]).strip(),
        "PRINCIPIO_ATIVO": str(row["PRINCIPIO_ATIVO"]).strip(),
        "CLASSE_TERAPEUTICA": str(row["CLASSE_TERAPEUTICA"]).strip(),
        "EMPRESA": str(row["EMPRESA_DETENTORA_REGISTRO"]).strip(),
    }
    documents.append(Document(page_content=text, metadata=metadata))

print(f"{len(documents)} documentos criados para o vector store.")

# ============================================
# 4. Criar vector store com embeddings
# ============================================

print("Criando vector store (isso pode demorar alguns minutos)...")
db = Chroma.from_documents(
    documents,
    embedding_function,
    persist_directory="../app/data/vectorstores/medicacoes_db"
)

print("✅ Vector store criado com embeddings!")