from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from server.auth.routes import router as auth_router
# from server.reports.routes import router as report_router
# from server.diagnosis.routes import router as diagnosis_router


app=FastAPI(title="RBAC Medical Report Diagnosis")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(auth_router)
# app.include_router(report_router)
# app.include_router(diagnosis_router)