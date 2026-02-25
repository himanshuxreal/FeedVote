from sqlalchemy.orm import Session
from sqlalchemy import func, and_, case
from app import models, schemas


# ==================== User CRUD ====================

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """Create a new user"""
    db_user = models.User(username=user.username, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_id(db: Session, user_id: int) -> models.User:
    """Get user by ID"""
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str) -> models.User:
    """Get user by username"""
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_email(db: Session, email: str) -> models.User:
    """Get user by email"""
    return db.query(models.User).filter(models.User.email == email).first()


def get_all_users(db: Session, skip: int = 0, limit: int = 100):
    """Get all users with pagination"""
    return db.query(models.User).offset(skip).limit(limit).all()


# ==================== Feedback CRUD ====================

def create_feedback(db: Session, feedback: schemas.FeedbackCreate, user_id: int) -> models.Feedback:
    """Create new feedback"""
    db_feedback = models.Feedback(
        title=feedback.title,
        description=feedback.description,
        user_id=user_id
    )
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback


def get_feedback_by_id(db: Session, feedback_id: int) -> models.Feedback:
    """Get feedback by ID"""
    return db.query(models.Feedback).filter(models.Feedback.id == feedback_id).first()


def get_all_feedback(db: Session, skip: int = 0, limit: int = 100):
    """Get all feedback with pagination"""
    return db.query(models.Feedback).order_by(models.Feedback.created_at.desc()).offset(skip).limit(limit).all()


def get_feedback_with_vote_count(db: Session, skip: int = 0, limit: int = 100):
    """Get feedback with vote counts"""
    feedback_list = db.query(models.Feedback).offset(skip).limit(limit).all()
    result = []
    for feedback in feedback_list:
        upvotes = db.query(func.count(models.Vote.id)).filter(
            and_(
                models.Vote.feedback_id == feedback.id,
                models.Vote.vote_type == models.VoteType.UPVOTE
            )
        ).scalar()
        downvotes = db.query(func.count(models.Vote.id)).filter(
            and_(
                models.Vote.feedback_id == feedback.id,
                models.Vote.vote_type == models.VoteType.DOWNVOTE
            )
        ).scalar()
        result.append({
            'feedback': feedback,
            'vote_count': upvotes - downvotes,
            'upvotes': upvotes,
            'downvotes': downvotes
        })
    return result


def get_top_ideas(db: Session, limit: int = 10):
    """Get top voted ideas (ordered by vote count)"""
    # Get all feedback ordered by ID
    all_feedback = db.query(models.Feedback).all()
    
    # Calculate vote counts for each feedback
    ideas_with_votes = []
    for feedback in all_feedback:
        upvotes = db.query(func.count(models.Vote.id)).filter(
            and_(
                models.Vote.feedback_id == feedback.id,
                models.Vote.vote_type == models.VoteType.UPVOTE
            )
        ).scalar() or 0
        
        downvotes = db.query(func.count(models.Vote.id)).filter(
            and_(
                models.Vote.feedback_id == feedback.id,
                models.Vote.vote_type == models.VoteType.DOWNVOTE
            )
        ).scalar() or 0
        
        net_votes = upvotes - downvotes
        username = feedback.user.username if feedback.user else "Unknown"
        
        ideas_with_votes.append({
            'id': feedback.id,
            'title': feedback.title,
            'description': feedback.description,
            'vote_count': net_votes,
            'upvotes': upvotes,
            'downvotes': downvotes,
            'username': username,
            'created_at': feedback.created_at
        })
    
    # Sort by vote count (descending) and return top N
    sorted_ideas = sorted(ideas_with_votes, key=lambda x: x['vote_count'], reverse=True)
    return sorted_ideas[:limit]


def delete_feedback(db: Session, feedback_id: int) -> bool:
    """Delete feedback by ID"""
    feedback = db.query(models.Feedback).filter(models.Feedback.id == feedback_id).first()
    if feedback:
        db.delete(feedback)
        db.commit()
        return True
    return False


# ==================== Vote CRUD ====================

def create_vote(db: Session, vote: schemas.VoteCreate) -> models.Vote:
    """Create new vote"""
    # Check for duplicate vote (prevent user from voting twice on same feedback)
    existing_vote = get_user_vote_on_feedback(db, vote.user_id, vote.feedback_id)
    if existing_vote:
        # Update existing vote
        existing_vote.vote_type = vote.vote_type
        db.commit()
        db.refresh(existing_vote)
        return existing_vote
    
    db_vote = models.Vote(
        feedback_id=vote.feedback_id,
        user_id=vote.user_id,
        vote_type=vote.vote_type
    )
    db.add(db_vote)
    db.commit()
    db.refresh(db_vote)
    return db_vote


def get_user_vote_on_feedback(db: Session, user_id: int, feedback_id: int) -> models.Vote:
    """Get user's vote on specific feedback (prevent duplicate votes)"""
    return db.query(models.Vote).filter(
        and_(
            models.Vote.user_id == user_id,
            models.Vote.feedback_id == feedback_id
        )
    ).first()


def get_votes_for_feedback(db: Session, feedback_id: int):
    """Get all votes for specific feedback"""
    return db.query(models.Vote).filter(models.Vote.feedback_id == feedback_id).all()


def get_vote_count_for_feedback(db: Session, feedback_id: int) -> dict:
    """Get vote count (upvotes - downvotes) for feedback"""
    upvotes = db.query(func.count(models.Vote.id)).filter(
        and_(
            models.Vote.feedback_id == feedback_id,
            models.Vote.vote_type == models.VoteType.UPVOTE
        )
    ).scalar() or 0
    
    downvotes = db.query(func.count(models.Vote.id)).filter(
        and_(
            models.Vote.feedback_id == feedback_id,
            models.Vote.vote_type == models.VoteType.DOWNVOTE
        )
    ).scalar() or 0
    
    return {
        'upvotes': upvotes,
        'downvotes': downvotes,
        'net_votes': upvotes - downvotes
    }


def delete_vote(db: Session, vote_id: int) -> bool:
    """Delete vote by ID"""
    vote = db.query(models.Vote).filter(models.Vote.id == vote_id).first()
    if vote:
        db.delete(vote)
        db.commit()
        return True
    return False
