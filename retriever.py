"""
Local RAG retrieval system using FREE sentence-transformers for embeddings
NO OpenAI API required!
"""
import chromadb
from chromadb.config import Settings
from typing import List, Dict, Optional
from sentence_transformers import SentenceTransformer
from config import config


class ClinicalRAGRetriever:
    """Vector-based retrieval system using FREE local embeddings"""
    
    def __init__(self):
        self.client = chromadb.PersistentClient(
            path=config.VECTOR_DB_PATH,
            settings=Settings(anonymized_telemetry=False)
        )
        self.collection = None
        
        # Load FREE local embedding model
        print(f"Loading local embedding model: {config.LOCAL_EMBEDDING_MODEL}")
        self.embedding_model = SentenceTransformer(config.LOCAL_EMBEDDING_MODEL)
        print("✓ Local embedding model loaded (100% FREE!)")
    
    def create_collection(self, collection_name: str = None):
        """Create or get collection"""
        name = collection_name or config.COLLECTION_NAME
        
        # Delete existing collection if it exists
        try:
            self.client.delete_collection(name=name)
        except:
            pass
        
        self.collection = self.client.create_collection(
            name=name,
            metadata={"hnsw:space": "cosine"}
        )
        print(f"Created collection: {name}")
    
    def get_collection(self, collection_name: str = None):
        """Get existing collection"""
        name = collection_name or config.COLLECTION_NAME
        try:
            self.collection = self.client.get_collection(name=name)
            print(f"Loaded collection: {name}")
        except:
            print(f"Collection {name} not found. Creating new one...")
            self.create_collection(name)
    
    def get_embedding(self, text: str) -> List[float]:
        """Get embedding from FREE local model"""
        embedding = self.embedding_model.encode(text, convert_to_tensor=False)
        return embedding.tolist()
    
    def add_chunks(self, chunks: List[Dict[str, str]]):
        """Add chunks to the vector database"""
        if not self.collection:
            self.get_collection()
        
        # Prepare data for ChromaDB
        ids = []
        documents = []
        metadatas = []
        embeddings = []
        
        print(f"Generating embeddings for {len(chunks)} chunks (FREE - no API costs!)...")
        
        for chunk in chunks:
            ids.append(chunk["chunk_id"])
            documents.append(chunk["text"])
            metadatas.append({
                "section": chunk["section"],
                "patient_id": chunk.get("patient_id", "unknown")
            })
            
            # Get embedding from FREE local model
            embedding = self.get_embedding(chunk["text"])
            embeddings.append(embedding)
        
        # Add to collection
        self.collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
            embeddings=embeddings
        )
        
        print(f"✓ Added {len(chunks)} chunks to collection")
    
    def retrieve(self, query: str, k: int = None) -> List[Dict[str, str]]:
        """
        Retrieve top K most relevant chunks for a query
        
        Returns:
            List of chunks with chunk_id, section, text, and distance
        """
        if not self.collection:
            self.get_collection()
        
        k = k or config.RETRIEVAL_K
        
        # Get query embedding from FREE local model
        query_embedding = self.get_embedding(query)
        
        # Query the collection
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k
        )
        
        # Format results
        chunks = []
        for i in range(len(results['ids'][0])):
            chunks.append({
                "chunk_id": results['ids'][0][i],
                "section": results['metadatas'][0][i].get('section', 'UNKNOWN'),
                "text": results['documents'][0][i],
                "distance": results['distances'][0][i] if 'distances' in results else 0.0
            })
        
        return chunks
    
    def clear_collection(self):
        """Clear all data from collection"""
        if self.collection:
            try:
                self.client.delete_collection(name=config.COLLECTION_NAME)
                print(f"Cleared collection: {config.COLLECTION_NAME}")
            except:
                pass


if __name__ == "__main__":
    # Test the local retriever
    from chunker import ClinicalNoteChunker
    
    sample_note = """
Chief Complaint:
Fever, cough, and shortness of breath

History of Present Illness:
Mr. Sharma, 65-year-old male, presents with fever (38.9°C), productive cough, and shortness of breath for 3 days.

Imaging:
Chest X-ray shows right lower lobe consolidation consistent with lobar pneumonia.

Laboratory:
WBC 16.5 x10^9/L (elevated), CRP 120 mg/L (elevated).
"""
    
    # Create chunks
    chunker = ClinicalNoteChunker()
    chunks = chunker.process_note(sample_note, patient_id="PT001")
    
    # Initialize LOCAL retriever (FREE!)
    retriever = ClinicalRAGRetriever()
    retriever.create_collection()
    retriever.add_chunks(chunks)
    
    # Test retrieval
    query = "What are the patient's symptoms and lab findings?"
    results = retriever.retrieve(query, k=3)
    
    print(f"\nRetrieved {len(results)} chunks:")
    for chunk in results:
        print(f"\n{chunk['chunk_id']} ({chunk['section']}) - Distance: {chunk['distance']:.4f}")
        print(f"  {chunk['text'][:100]}...")
