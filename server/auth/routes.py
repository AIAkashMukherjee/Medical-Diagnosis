from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from .models import SignupRequest
from .hash import hash_password, verify_password
from ..config.db import users_collection

router=APIRouter(prefix='/auth',tags=['auth'])
security=HTTPBasic()

@router.post('/signup')
def signup(user:SignupRequest):
    if users_collection.find_one({'username':user.username}):
        raise HTTPException(status_code=400,detail='User already exists')
    
    users_collection.insert_one({
        'username':user.username,
        'password':hash_password(user.password),
        'role':user.role
    })
    return {'message':'User created successfully'}


def authenticate(credentials:HTTPBasicCredentials=Depends(security)):
    user=users_collection.find_one({'username':credentials.username })
    if not user or not verify_password(credentials.password,user['password']):
        raise HTTPException(status_code=401,detail='Invalid credentials')
    return {'username':user['username'],'role':user['role']}

@router.get("/login")
def login(user=Depends(authenticate)):
    return {'username':user['username'],'role':user['role']}
