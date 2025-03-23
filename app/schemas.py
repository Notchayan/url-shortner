from pydantic import BaseModel, HttpUrl, validator
from typing import Optional
from datetime import datetime
import re

class URLBase(BaseModel):
    original_url: str  # Use str instead of HttpUrl for more flexible validation
    
    @validator('original_url')
    def validate_url(cls, v):
        # Add your own URL validation logic here
        if not v.startswith(('http://', 'https://')):
            raise ValueError('URL must start with http:// or https://')
        return v

class URLCreate(URLBase):
    alias: Optional[str] = None
    expires_days: Optional[int] = None
    
    @validator('alias')
    def validate_alias(cls, v):
        if v is not None:
            if len(v) < 4:
                raise ValueError('Alias must be at least 4 characters')
            if not v.isalnum():
                raise ValueError('Alias must be alphanumeric')
        return v

class URLResponse(URLBase):
    short_code: str
    short_url: str
    created_at: datetime
    expires_at: Optional[datetime] = None
    click_count: int

    class Config:
        from_attributes = True

class URLStats(BaseModel):
    short_code: str
    original_url: HttpUrl
    created_at: datetime
    expires_at: Optional[datetime] = None
    click_count: int

    class Config:
        from_attributes = True