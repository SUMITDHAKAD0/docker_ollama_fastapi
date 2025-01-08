from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableMap
from langchain_core.documents import Document
from langchain_ollama import ChatOllama, OllamaEmbeddings
from src.vectorstore_milvus import MilvusVectorStoreManager
import os 
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings


class ChatGenerator:
    def __init__(self):
        pass

    def load_model(self):
        # ollama_llm = ChatOllama(
        #     model= 'llama3.2-vision',
        #     base_url="http://localhost:11434",
        #     temperature=0.7,
        #     num_ctx = 1024, # size of the context window
        #     num_predict = -2, # Maximum number of tokens to predict when generating text.
        #     top_k=40,
        #     top_p=0.9,  
        # )

        # ollama_embedding = OllamaEmbeddings(
        #     model="llama3.2-vision",
        #     base_url="http://localhost:11434"
        # )
        # return ollama_llm, ollama_embedding
        os.environ["GOOGLE_API_KEY"] = "AIzaSyAI1sh_VTt7WUSrZ8UX4T4yRxRoEcaXNvg"
        gemini_embeddings = GoogleGenerativeAIEmbeddings(
                                model="models/text-embedding-004",
                                task_type="retrieval_document"
                            )

        gemini_llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", 
                                    temperature=0.7,
                                    max_tokens=512,
                                    timeout=None,
                                    max_retries=2,
                                    top_k=90,
                                    top_p=0.5
                                )
        return gemini_llm, gemini_embeddings
    
    def load_and_splite(self):
        loader = PyPDFLoader('data/B13 - Chapter II - Procedure  for proceeding Abroad.pdf')
        documents = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1200,
            chunk_overlap=200,
            length_function=len,
            is_separator_regex=False,
        )

        chunks = text_splitter.split_documents(documents)
        return chunks
    

    def vector(self, embedding, text_chunks):
        milvus_manager = MilvusVectorStoreManager(
            embeddings=embedding, 
            collection_name='test_collection'
        )
        
        vectorstore = milvus_manager.create_collection(text_chunks)

        # Define the search parameters
        search_kwargs = {"k": 5, "ef": 10}  # Ensure ef >= k

        # Create the individual retrievers with the search parameters
        retriever = vectorstore.as_retriever(
                search_type="similarity", 
                search_kwargs=search_kwargs
            )
        
        return retriever
    
    def chat_generator(self, retriever, ollama_llm):
        # Define the prompt template

        prompt = ChatPromptTemplate.from_template("""                                
                        Please analyze the following text and provide a summary or key insights based on its 
                        content: {context} + {question}

                        Question: {question}
                        If there are no clear questions, please offer general information or commentary 
                        related to the themes and topics presented.
                    """)


        # Define the pipeline
        chain = (
                RunnableMap({
                    "context": retriever,  # Use your retriever here
                    "question": RunnablePassthrough()  # Pass
                })
                | prompt 
                | ollama_llm 
                | StrOutputParser() 
            )
        
        return chain
    

    def main(self):
        model, embedding = self.load_model()
        chunks = self.load_and_splite()
        retriever = self.vector(embedding, chunks)
        chain = self.chat_generator(retriever, model)

        return chain
    

def chat_main(query):
    obj = ChatGenerator()
    chain = obj.main()
    return chain.invoke(query)




    
