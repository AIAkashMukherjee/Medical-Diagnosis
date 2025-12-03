import os
import asyncio
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "rbac-diagnosis-index")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GPT_API_KEY=os.getenv("GPT_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV", "us-east-1")

pc=Pinecone(api_key=PINECONE_API_KEY)
index=pc.Index(PINECONE_INDEX_NAME)

embed_model=HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")       
llm=ChatGroq(temperature=0,model="llama-3.1-8b-instant")

prompt=PromptTemplate.from_template("""
You are a medical assistant. Using the provided context (fragments of the user's report), please produce the following:

Concise Probable Diagnosis:
    Provide a brief statement (1-2 lines) identifying the most likely diagnosis based on the context.
Key Findings from the Report:
    List the most relevant findings, highlighting symptoms and any notable details using bullet points.
Recommended Next Steps:
Clearly label as suggestions (not medical advice) and include:
    Suggested tests that may be helpful for further assessment.
    Suggested treatments or interventions that could be considered.
Context:
{context}

User question:
{query}                                    
                                    
""")

rag_chain=prompt | llm

async def get_diagnosis(query:str,username:str,doc_id:str):
    # question embed
    emebedding=await asyncio.to_thread(embed_model.embed_query,query)
    
    # query pinecone
    result=await asyncio.to_thread(index.query,vector=emebedding,top_k=5,include_metadata=True)
    
    # filter for doc_id match
    contexts=[]
    source_set=set()
    for match in result.get('matches',[]):
        md=match.get('metadata',{})
        if md.get('doc_id')==doc_id:
            # take text snippet
            text_snippet=md.get("text") or ""
            contexts.append(text_snippet)
            source_set.add(md.get('source'))
    
    if not contexts:
        return {
            "diagnosis":None,"explanation":"No relevant report sections found for the provided document ID."
        }        
    
        # limit context size
    context_text="\n\n".join(contexts[:6])
    
    # final call rag chain
    final=await asyncio.to_thread(rag_chain.invoke,{"context":context_text,"query":query})
    return {
        'diagnosis':final.content,
        "sources":list(source_set)
    }
     
        