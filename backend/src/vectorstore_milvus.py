import os
from pymilvus import MilvusClient
# from langchain_milvus import Milvus
from langchain_milvus_updated.vectorstores.milvus import Milvus
from langchain_core.documents import Document
from pymilvus import connections, utility, Collection
from src.logging_config import logger


# class MilvusVectorStoreManager:
#     def __init__(self, embeddings, collection_name='hr_documents_collection', host='localhost', port='19530'):
#         """
#         Initialize Milvus Vector Store
        
#         :param embeddings: Embedding model
#         :param collection_name: Name of the Milvus collection
#         :param host: Milvus server host
#         :param port: Milvus server port
#         """
#         # Initialize embeddings 
#         self.embeddings = embeddings
        
#         # Connection parameters
#         self.connection_args = {
#             'host': host,
#             'port': port,
#         }
        
#         self.collection_name = collection_name
    
#     def create_collection(self, documents=None):
#         """
#         Create a new vector store in Milvus
        
#         :param documents: List of documents to store
#         :return: Milvus Vector Store
#         """
#         try:
        
#             vector_store = Milvus.from_documents(
#                 documents=documents,
#                 embedding=self.embeddings,
#                 collection_name=self.collection_name,
#                 connection_args={'uri': 'database/milvushr.db'},
#                 drop_old=True,
#             )
#             logger.info(f"Successfully created new collection {self.collection_name} with {len(documents)} of documents")
#             return vector_store
#         except Exception as e:
#             logger.error(f"Error creating vector store: {e}")
#             return None
    

#     def load_existing_collection(self):
#         """
#         Load an existing Milvus vector store
        
#         :return: Existing Milvus Vector Store
#         """
#         try:
#             vector_store = Milvus(
#                 self.embeddings,
#                 connection_args={'uri': 'database/milvus.db'},
#                 collection_name=self.collection_name,
#             )
#             logger.info(f"Successfully loaded existing vector store: {self.collection_name} with  records")
#             return vector_store
#         except Exception as e:
#             logger.error(f"Error loading vector store: {e}")
#             return None
    

#     def add_documents(self, vector_store, documents):
#         """
#         Add new documents to an existing vector store
        
#         :param vector_store: Existing Milvus Vector Store
#         :param documents: List of new documents to add
#         :return: List of document IDs or None
#         """
#         try:
#             doc_ids = vector_store.add_documents(documents)
#             logger.info(f"Successfully added {len(documents)} documents to vector store")
#             return doc_ids
#         except Exception as e:
#             logger.error(f"Error adding documents: {e}")
#             return None


#     def list_collections(self):
#         """
#         List all collections in Milvus
        
#         :return: List of collection names
#         """
#         try:
#             collections = utility.list_collections()
#             logger.info(f"Successfully retrieved list of {len(collections)} collections")
#             return collections
#         except Exception as e:
#             logger.error(f"Error listing collections: {e}")
#             return []
    

#     def count_records(self, collection_name=None):
#         """
#         Count records in all or specific collections
        
#         :param collection_name: Optional specific collection name
#         :return: Dictionary of collection names and their record counts
#         """
#         collection_counts = {}
        
#         try:
#             # If a specific collection is provided
#             if collection_name:
#                 collection = Collection(collection_name)
#                 collection_counts[collection_name] = collection.num_entities
#                 logger.info(f"Counted {collection_counts[collection_name]} records in collection {collection_name}")
#                 return collection_counts
            
#             # Count for all collections
#             for name in utility.list_collections():
#                 collection = Collection(name)
#                 collection_counts[name] = collection.num_entities
            
#             # logger.info(f"Successfully counted records in {len(collection_counts)} collections")
#             return collection_counts
#         except Exception as e:
#             logger.error(f"Error counting records: {e}")
#             return collection_counts
    

#     def print_collection_summary(self):
#         """
#         Print a summary of all collections and their record counts
#         """
#         logger.info("Generating Milvus Collection Summary")
#         print("Milvus Collection Summary:")
#         print("-" * 30)
        
#         try:
#             collections = self.list_collections()
#             print(f"Total Collections: {len(collections)}")
            
#             record_counts = self.count_records()
#             for name, count in record_counts.items():
#                 print(f"Collection: {name}, Records: {count}")
#             logger.info("Successfully printed collection summary")
#         except Exception as e:
#             logger.error(f"Error printing collection summary: {e}")


#     def delete_collection(self, collection_name=None):
#         """
#         Delete a collection from Milvus
        
#         :param collection_name: Name of collection to delete. If None, deletes the default collection
#         :return: Boolean indicating success
#         """
#         name = collection_name if collection_name else self.collection_name
#         if self.client.has_collection(name):
#             self.client.drop_collection(name)
#             logger.info(f"Successfully deleted collection: {name}")
#             return True
#         else:
#             logger.warning(f"Collection {name} does not exist")
#             return False
        





class MilvusVectorStoreManager:
    def __init__(self, embeddings, collection_name='documents', host='localhost', port='19530'):
        """
        Initialize Milvus Vector Store
        
        :param embeddings: Embedding model
        :param collection_name: Name of the Milvus collection
        :param host: Milvus server host
        :param port: Milvus server port
        """
        os.makedirs('database', exist_ok=True)
        # Initialize embeddings 
        self.embeddings = embeddings
        
        # Connection parameters
        self.connection_args = {
            'uri' : "database/milvushr.db"
        }
        
        self.collection_name = collection_name
        # if self.client.has_collection('test_collection'):
        #     self.client.colse()
        #     print('connection closed')
        try:
            # Create Milvus client
            self.client = MilvusClient(
                    self.connection_args['uri']
                )
            logger.info(f"Connected to Milvus at {self.connection_args}")
        except Exception as e:
            logger.error(f"Error connecting to Milvus: {e}")


    
    def create_collection(self, documents=None):
        """
        Create a new vector store in Milvus
        
        :param documents: List of documents to store
        :return: Milvus Vector Store
        """
        try:
            vector_store = Milvus.from_documents(
                documents,
                self.embeddings,
                connection_args=self.connection_args,
                collection_name=self.collection_name,
                auto_id=True
            )
            self.client.close()
            logger.info(f"Successfully created new collection {self.collection_name} with {len(documents)} of documents")
            return vector_store
        except Exception as e:
            logger.error(f"Error creating vector store: {e}")
            return None
    

    def load_collection(self):
        """
        Load an existing Milvus vector store
        
        :return: Existing Milvus Vector Store
        """
        try:
            vector_store = Milvus(
                self.embeddings, 
                connection_args=self.connection_args, 
                collection_name=self.collection_name,
                auto_id=True
            )
            self.client.close()
            logger.info(f"Successfully loaded existing vector store: {self.collection_name} with {vector_store.col.num_entities} records")
            return vector_store
        except Exception as e:
            logger.error(f"Error loading vector store: {e}")
            return None
    

    def add_documents(self, vector_store, documents):
        """
        Add new documents to an existing vector store
        
        :param vector_store: Existing Milvus Vector Store
        :param documents: List of new documents to add
        :return: List of document IDs or None
        """
        try:
            doc_ids = vector_store.add_documents(documents)
            logger.info(f"Successfully added {len(documents)} documents to vector store")
            self.client.close()
            return doc_ids
        except Exception as e:
            logger.error(f"Error adding documents: {e}")
            return None
    

    def get_collection_summary(self):
        """
        Print a summary of all collections and their record counts
        """
        logger.info("Generating Milvus Collection Summary")
        print("Milvus Collection Summary:")
        print("-" * 30)
        
        try:
            collections = self.client.list_collections()
            print(f"Total Collections: {len(collections)}")

            for name in collections:
                print(f"Collection Name : {name} ----- No. of Records : {self.client.get_collection_stats(name)['row_count']}")
            print("-" * 30)
            self.client.close()
            logger.info("Successfully printed collection summary")
        except Exception as e:
            logger.error(f"Error printing collection summary: {e}")


    def delete_collection(self, collection_name=None):
        """
        Delete a collection from Milvus
        
        :param collection_name: Name of collection to delete. If None, deletes the default collection
        :return: Boolean indicating success
        """
        name = collection_name if collection_name else self.collection_name
        if self.client.has_collection(name):
            self.client.drop_collection(name)
            logger.info(f"Successfully deleted collection: {name}")
            self.client.close()
            return True
        else:
            logger.warning(f"Collection {name} does not exist")
            return False

