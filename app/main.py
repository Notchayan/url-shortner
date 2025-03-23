from fastapi import FastAPI, HTTPException, Depends, Request, status
from fastapi.responses import RedirectResponse, JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_, and_
from datetime import datetime, timezone
import validators
from typing import Optional
import logging

from .database import get_db, engine
from . import models, schemas, utils

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="URL Shortener API")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates
templates = Jinja2Templates(directory="app/templates")

BASE_URL = "http://localhost:8000"  # Change in production

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    """Home page with URL shortening form"""
    # Get recent URLs (limit to 5) for display
    recent_urls = db.query(models.URL).order_by(models.URL.created_at.desc()).limit(5).all()
    
    # Add the full short URL to each result
    for url in recent_urls:
        url.short_url = f"{BASE_URL}/{url.short_code}"
    
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "recent_urls": recent_urls}
    )

@app.post("/shorten", response_model=schemas.URLResponse, status_code=status.HTTP_201_CREATED)
def create_short_url(url_create: schemas.URLCreate, db: Session = Depends(get_db)):
    """Create a shortened URL. Optionally provide a custom alias and expiration time."""
    
    # Validate the URL
    if not validators.url(url_create.original_url):
        raise HTTPException(status_code=400, detail="Invalid URL")
    
    # Check if the URL already exists and not expired
    existing_url = db.query(models.URL).filter(
        models.URL.original_url == str(url_create.original_url),
        or_(
            models.URL.expires_at.is_(None),
            models.URL.expires_at > datetime.now()
        )
    ).first()
    
    if existing_url and not url_create.alias:
        # Return the existing short URL if found and no custom alias is requested
        existing_url.short_url = f"{BASE_URL}/{existing_url.short_code}"
        return existing_url
    
    # Handle custom alias if provided
    if url_create.alias:
        # Check if alias already exists
        existing_alias = db.query(models.URL).filter(models.URL.short_code == url_create.alias).first()
        if existing_alias:
            raise HTTPException(status_code=400, detail="Custom alias already in use")
        short_code = url_create.alias
        custom_alias = True
    else:
        # Generate short code based on the URL
        short_code = utils.generate_short_code(str(url_create.original_url))
        custom_alias = False
    
    # Calculate expiration date if provided
    expires_at = utils.calculate_expiration_date(url_create.expires_days)
    
    # Create a new URL entry
    db_url = models.URL(
        original_url=str(url_create.original_url),
        short_code=short_code,
        custom_alias=custom_alias,
        expires_at=expires_at,
        click_count=0
    )
    
    try:
        db.add(db_url)
        db.commit()
        db.refresh(db_url)
        
        # Add short_url to the response
        db_url.short_url = f"{BASE_URL}/{db_url.short_code}"
        return db_url
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="URL processing error")

@app.get("/{short_code}", response_class=RedirectResponse)
def redirect_to_url(short_code: str, request: Request, db: Session = Depends(get_db)):
    """Redirect to the original URL based on the short code."""
    
    # Find the URL in the database
    db_url = db.query(models.URL).filter(models.URL.short_code == short_code).first()
    
    if not db_url:
        raise HTTPException(status_code=404, detail="URL not found")
    
    # Check if the URL has expired
    if db_url.expires_at and db_url.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=410, detail="URL has expired")
    
    # Increment the click count
    db_url.click_count += 1
    db.commit()
    
    # Redirect to the original URL
    return RedirectResponse(url=db_url.original_url)

@app.get("/stats/{short_code}", response_model=schemas.URLStats)
def get_url_stats(short_code: str, db: Session = Depends(get_db)):
    """Get statistics for a shortened URL."""
    
    db_url = db.query(models.URL).filter(models.URL.short_code == short_code).first()
    
    if not db_url:
        raise HTTPException(status_code=404, detail="URL not found")
    
    return db_url

@app.delete("/{short_code}", status_code=status.HTTP_204_NO_CONTENT)
def delete_url(short_code: str, db: Session = Depends(get_db)):
    """Delete a shortened URL."""
    
    db_url = db.query(models.URL).filter(models.URL.short_code == short_code).first()
    
    if not db_url:
        raise HTTPException(status_code=404, detail="URL not found")
    
    db.delete(db_url)
    db.commit()
    
    return None

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logging.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)},
    )