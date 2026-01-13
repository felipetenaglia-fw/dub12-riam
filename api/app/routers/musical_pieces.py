from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.user import User, UserRole
from ..models.musical_piece import MusicalPiece
from ..schemas.musical_piece import MusicalPieceCreate, MusicalPieceUpdate, MusicalPieceResponse
from ..auth import get_current_user, require_teacher

router = APIRouter(prefix="/pieces", tags=["Musical Pieces"])


@router.get("", response_model=List[MusicalPieceResponse])
def list_musical_pieces(
    composer: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List all musical pieces. All authenticated users.
    Can filter by composer.
    """
    query = db.query(MusicalPiece)
    if composer:
        query = query.filter(MusicalPiece.composer.ilike(f"%{composer}%"))
    pieces = query.all()
    return pieces


@router.get("/{piece_id}", response_model=MusicalPieceResponse)
def get_musical_piece(
    piece_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get musical piece by ID.
    """
    piece = db.query(MusicalPiece).filter(MusicalPiece.id == piece_id).first()
    if not piece:
        raise HTTPException(status_code=404, detail="Musical piece not found")
    return piece


@router.post("", response_model=MusicalPieceResponse, status_code=status.HTTP_201_CREATED)
def create_musical_piece(
    piece_data: MusicalPieceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher)
):
    """
    Create a new musical piece. Teachers and admins only.
    """
    piece = MusicalPiece(
        title=piece_data.title,
        composer=piece_data.composer,
        description=piece_data.description,
        audio_url=piece_data.audio_url
    )
    db.add(piece)
    db.commit()
    db.refresh(piece)
    return piece


@router.put("/{piece_id}", response_model=MusicalPieceResponse)
def update_musical_piece(
    piece_id: int,
    piece_data: MusicalPieceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher)
):
    """
    Update musical piece. Teachers and admins only.
    """
    piece = db.query(MusicalPiece).filter(MusicalPiece.id == piece_id).first()
    if not piece:
        raise HTTPException(status_code=404, detail="Musical piece not found")
    
    if piece_data.title is not None:
        piece.title = piece_data.title
    if piece_data.composer is not None:
        piece.composer = piece_data.composer
    if piece_data.description is not None:
        piece.description = piece_data.description
    if piece_data.audio_url is not None:
        piece.audio_url = piece_data.audio_url
    
    db.commit()
    db.refresh(piece)
    return piece
