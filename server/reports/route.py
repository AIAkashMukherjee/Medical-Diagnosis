from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from server.auth.routes import authenticate
from server.reports.vectorestore import load_vectorstore
import uuid
from typing import List
from ..config.db import reports_collection

router=APIRouter(prefix="/reports",tags=["reports"])

@router.post("/upload")
async def upload_reports(user=Depends(authenticate),files:List[UploadFile]=File(...)): # ... object format
    if user['role']!='patient':
        raise HTTPException(status_code=403,detail="Only patients can upload reports")
    
    doc_id=str(uuid.uuid4())
    await load_vectorstore(files,user['username'],doc_id)
    return {"message":"Uploaded and indexed","doc_id":doc_id}