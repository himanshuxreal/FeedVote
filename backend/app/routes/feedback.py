from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, schemas, database, models

router = APIRouter(prefix="/feedback", tags=["feedback"])


@router.post("/", response_model=schemas.Feedback, status_code=status.HTTP_201_CREATED)
def create_feedback(
    feedback: schemas.FeedbackCreate,
    user_id: int,
    db: Session = Depends(database.get_db)
):
    """Create new feedback"""
    # Validate user exists
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Create feedback
    db_feedback = crud.create_feedback(db, feedback, user_id)
    return db_feedback


@router.get("/", response_model=list[schemas.Feedback])
def get_all_feedback(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(database.get_db)
):
    """Get all feedback with pagination"""
    if skip < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Skip must be >= 0"
        )
    if limit < 1 or limit > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Limit must be between 1 and 100"
        )
    
    feedback_list = crud.get_all_feedback(db, skip=skip, limit=limit)
    return feedback_list


@router.get("/{feedback_id}", response_model=schemas.Feedback)
def get_feedback_by_id(
    feedback_id: int,
    db: Session = Depends(database.get_db)
):
    """Get feedback by ID"""
    if feedback_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Feedback ID must be greater than 0"
        )
    
    feedback = crud.get_feedback_by_id(db, feedback_id)
    if not feedback:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feedback not found"
        )
    
    return feedback
