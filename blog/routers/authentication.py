import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from .. import models, database
from sqlalchemy.orm import Session
from ..hashing import Hash
from ..JWTtoken import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(
    prefix='/login',
    tags=['Authentication']
)


@router.post('/')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session=Depends(database.get_db)):
    user = db.query(models.Users).filter(models.Users.email == request.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
    
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Password")
    
    # generate JWT token and return
    access_token_expires = datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
