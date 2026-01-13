from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.user import User, UserRole
from ..schemas.user import UserCreate, UserUpdate, UserResponse
from ..auth import get_current_user, require_admin, get_password_hash

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", response_model=List[UserResponse])
def list_users(
    role: UserRole = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    List all users. Admin only.
    Can filter by role.
    """
    query = db.query(User)
    if role:
        query = query.filter(User.role == role)
    users = query.all()
    return users


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get user by ID.
    Admin can access any user. Others can only access their own data.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check permissions
    if current_user.role != UserRole.ADMIN and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Access forbidden")
    
    return user


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Create a new user. Admin only.
    """
    # Check if username already exists
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # Check if email already exists
    existing_email = db.query(User).filter(User.email == user_data.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    # Create user
    user = User(
        username=user_data.username,
        password_hash=get_password_hash(user_data.password),
        name=user_data.name,
        email=user_data.email,
        role=user_data.role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update user information.
    Admin can update any user. Others can only update their own data.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check permissions
    if current_user.role != UserRole.ADMIN and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Access forbidden")
    
    # Update fields
    if user_data.name is not None:
        user.name = user_data.name
    if user_data.email is not None:
        # Check if new email already exists
        existing_email = db.query(User).filter(
            User.email == user_data.email,
            User.id != user_id
        ).first()
        if existing_email:
            raise HTTPException(status_code=400, detail="Email already exists")
        user.email = user_data.email
    if user_data.password is not None:
        user.password_hash = get_password_hash(user_data.password)
    
    db.commit()
    db.refresh(user)
    
    return user
