from fastapi import APIRouter, Depends
from .. import schemas
from ..database import get_db
from sqlalchemy.orm import Session
from ..repository import user


router = APIRouter(
    prefix='/user',
    tags=['Users'],
)


@router.post('/', response_model=schemas.ShowUsers)
def create_user(request: schemas.Users, db: Session=Depends(get_db)):
    return user.create_user(request, db)


@router.get('/{id}', response_model=schemas.ShowUsers)
def show_user(id: int, db: Session=Depends(get_db)):
    return user.show_user(id, db)
