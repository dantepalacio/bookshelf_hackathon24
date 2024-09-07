import os
import openai
import asyncio

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_community.vectorstores import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain_core.prompts import MessagesPlaceholder

from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain.prompts.chat import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory 
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain import PromptTemplate

from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get('OPENAI_API_KEY')

openai.api_key = api_key



def read_text(file_content):

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    pages = text_splitter.split_text(file_content)

    return pages


def get_retrievers(pages):
    embeddings = OpenAIEmbeddings()

    bm25_retriever = BM25Retriever.from_texts(pages)
    bm25_retriever.k = 2

    faiss_vectorstore = FAISS.from_texts(pages, embeddings)
    faiss_retriever = faiss_vectorstore.as_retriever(search_kwargs={"k": 2})

    ensemble_retriever = EnsembleRetriever(retrievers=[bm25_retriever, faiss_retriever],weights=[0.6, 0.4])

    return ensemble_retriever


def get_chain(retriever):
    model = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.4
    )

    # Добавляем память для сохранения истории разговора
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    prompt = ChatPromptTemplate.from_messages([
        ("system","Ты интересный собеседник по книге. Твоя задача разговаривать с пользователем на тему заданного контекста. Отвечай ему развернуто, обязательно давай свою точку зрения на его вопросы и задавай ему встречные вопросы. Твоя задача максимально заинтересовать пользователя в разговоре по контексту.  \n Контекст: {context}"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "Вопрос пользователя: {input}")
    ])
    
    chain = create_stuff_documents_chain(
        llm=model,
        prompt=prompt,
    )

    retriever_prompt = ChatPromptTemplate.from_messages([
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        ("user", "Given the above conversation, generate a search query to look up in order to get information relevant to the conversation")
    ])
    history_aware_retriever = create_history_aware_retriever(
        llm=model,
        retriever=retriever,
        prompt=retriever_prompt
    )

    retrieval_chain = create_retrieval_chain(
        history_aware_retriever,
        chain
    )

    return retrieval_chain

