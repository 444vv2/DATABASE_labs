from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.base import get_db
from Service import ArtistService
from schemas.artist import ArtistCreate, ArtistUpdate, ArtistResponse

router = APIRouter(prefix="/artists", tags=["artists"])

@router.post("/", response_model=ArtistResponse, status_code=status.HTTP_201_CREATED)
async def create_artist(artist_data: ArtistCreate, db: AsyncSession = Depends(get_db)):
    """Створення артиста"""
    try:
        artist = await ArtistService.create_artist(db, artist_data)
        return artist
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) from e

@router.get("/{artist_id}", response_model=ArtistResponse)
async def get_artist_by_id(artist_id: int, db: AsyncSession = Depends(get_db)):
    """Отримання артиста за ID"""
    artist = await ArtistService.get_artist_by_id(db, artist_id)
    if not artist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Artist with id {artist_id} not found"
        )
    return artist

@router.get("/", response_model=List[ArtistResponse])
async def get_all_artists(db: AsyncSession = Depends(get_db)):
    """Отримання всіх артистів"""
    artists = await ArtistService.get_all_artists(db)
    return artists

@router.put("/{artist_id}", response_model=ArtistResponse)
async def update_artist(artist_id: int, artist_data: ArtistUpdate, db: AsyncSession = Depends(get_db)):
    """Оновлення артиста"""
    try:
        artist = await ArtistService.update_artist(db, artist_id, artist_data)
        if not artist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Artist with id {artist_id} not found"
            )
        return artist
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) from e

@router.delete("/{artist_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_artist(artist_id: int, db: AsyncSession = Depends(get_db)):
    """Видалення артиста"""
    try:
        deleted = await ArtistService.delete_artist_by_id(db, artist_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Artist with id {artist_id} not found"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        ) from e
