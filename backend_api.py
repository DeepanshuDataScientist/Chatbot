from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# FastAPI app initialization
app = FastAPI(title="ABS Chatbot API", version="1.0.0")

class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    answer: str
    response_time: float
    sources: list = []
    confidence: float = None

# Global variables for model components
embeddings = None
chain = None

def initialize_components():
    """Initialize the chatbot components"""
    global embeddings, chain
    try:
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        
        prompt_template = """
        Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
        provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
        Context:\n {context}?\n
        Question: \n{question}\n

        Answer:
        """
        
        model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
        prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
        chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
        
        logger.info("Components initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Error initializing components: {e}")
        return False

def get_answer(question: str):
    """Get answer from the chatbot"""
    try:
        # Check if FAISS index exists
        if not os.path.exists("faiss_index"):
            return "No document database found. Please upload and process documents first.", []
        
        # Load vector database
        new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
        
        # Perform similarity search
        docs = new_db.similarity_search(question, k=3)
        
        if not docs:
            return "No relevant documents found for your question.", []
        
        # Get response from chain
        response = chain(
            {"input_documents": docs, "question": question},
            return_only_outputs=True
        )
        
        # Extract sources
        sources = []
        for i, doc in enumerate(docs):
            source_info = {
                "source_id": i + 1,
                "content_preview": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
                "metadata": doc.metadata if hasattr(doc, 'metadata') else {}
            }
            sources.append(source_info)
        
        return response["output_text"], sources
        
    except Exception as e:
        logger.error(f"Error getting answer: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")

@app.on_event("startup")
async def startup_event():
    """Initialize components on startup"""
    success = initialize_components()
    if not success:
        logger.error("Failed to initialize components")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "ABS Chatbot API is running",
        "components_ready": embeddings is not None and chain is not None,
        "database_exists": os.path.exists("faiss_index")
    }

@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    """Process a question and return an answer"""
    start_time = time.time()
    
    try:
        # Validate components
        if embeddings is None or chain is None:
            raise HTTPException(status_code=503, detail="Chatbot components not initialized")
        
        # Get answer
        answer, sources = get_answer(request.question)
        
        response_time = time.time() - start_time
        
        return AnswerResponse(
            answer=answer,
            response_time=response_time,
            sources=sources,
            confidence=0.85  # You can implement actual confidence scoring
        )
        
    except HTTPException:
        raise
    except Exception as e:
        response_time = time.time() - start_time
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "ABS Chatbot API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "ask": "/ask",
            "docs": "/docs"
        }
    }

@app.get("/stats")
async def get_stats():
    """Get chatbot statistics"""
    return {
        "database_exists": os.path.exists("faiss_index"),
        "components_initialized": embeddings is not None and chain is not None,
        "api_version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)