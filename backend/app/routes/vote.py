from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, schemas, database

router = APIRouter(prefix="/vote", tags=["vote"])


@router.post("/", response_model=schemas.Vote, status_code=status.HTTP_201_CREATED)
def create_vote(
    vote: schemas.VoteCreate,
    db: Session = Depends(database.get_db)
):
    """Submit a vote (upvote or downvote)"""
    # Validate feedback exists
    feedback = crud.get_feedback_by_id(db, vote.feedback_id)
    if not feedback:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feedback not found"
        )
    
    # Validate user exists
    user = crud.get_user_by_id(db, vote.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if user is trying to vote on their own feedback
    if feedback.user_id == vote.user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot vote on your own feedback"
        )
    
    # Create vote (this will handle duplicate votes by updating)
    db_vote = crud.create_vote(db, vote)
    return db_vote


@router.get("/top/", response_model=list[schemas.TopIdea])
def get_top_ideas(
    limit: int = 10,
    db: Session = Depends(database.get_db)
):
    """Get top voted ideas (leaderboard)"""
    if limit < 1 or limit > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Limit must be between 1 and 100"
        )
    
    top_ideas = crud.get_top_ideas(db, limit=limit)
    return top_ideas
