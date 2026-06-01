from fastapi import FastAPI, HTTPException, Header, Request
from pydantic import BaseModel
from typing import Optional, List
import re
import hashlib
import time
from urllib.parse import urlparse

app = FastAPI(title="URL Metadata Extractor API", version="1.0.0")

# Rate limiting storage (in-memory for simplicity)
rate_limit_store = {}

def check_rate_limit(api_key: str, limit: int = 100, window: int = 3600) -> bool:
    now = time.time()
    key = f"rate_{api_key}"
    if key not in rate_limit_store:
        rate_limit_store[key] = {"count": 0, "reset": now + window}
    if now > rate_limit_store[key]["reset"]:
        rate_limit_store[key] = {"count": 0, "reset": now + window}
    if rate_limit_store[key]["count"] >= limit:
        return False
    rate_limit_store[key]["count"] += 1
    return True

def generate_api_key():
    return hashlib.md5(str(time.time()).encode()).hexdigest()[:16]

def mock_extract_metadata(url: str) -> dict:
    """Extract metadata from URL (mock implementation - in production would use aiohttp/requests-html)"""
    # Parse URL for basic info
    parsed = urlparse(url)
    domain = parsed.netloc.replace("www.", "")
    
    # Mock metadata extraction (would use actual scraping in production)
    return {
        "url": url,
        "domain": domain,
        "title": f"Page Title from {domain}",
        "description": f"Description of the page at {domain}",
        "image": f"https://{domain}/og-image.jpg",
        "url_type": "website",
        "site_name": domain.split(".")[0].title(),
        "favicon": f"https://{domain}/favicon.ico"
    }

class MetadataResponse(BaseModel):
    url: str
    domain: str
    title: str
    description: Optional[str] = None
    image: Optional[str] = None
    site_name: Optional[str] = None
    favicon: Optional[str] = None

class BulkRequest(BaseModel):
    urls: List[str]

@app.get("/health")
async def health():
    return {"status": "ok", "service": "url-metadata-extractor"}

@app.post("/extract")
async def extract_metadata(request: Request, api_key: str = Header(None)):
    if api_key is None or not check_rate_limit(api_key):
        raise HTTPException(status_code=429, detail="Rate limit exceeded or invalid API key")
    
    body = await request.json()
    url = body.get("url")
    
    if not url:
        raise HTTPException(status_code=400, detail="URL is required")
    
    if not re.match(r"^https?://", url):
        url = f"https://{url}"
    
    return mock_extract_metadata(url)

@app.post("/bulk")
async def bulk_extract(request: Request, api_key: str = Header(None)):
    if api_key is None or not check_rate_limit(api_key):
        raise HTTPException(status_code=429, detail="Rate limit exceeded or invalid API key")
    
    body = await request.json()
    urls = body.get("urls", [])
    
    if not urls or len(urls) > 10:
        raise HTTPException(status_code=400, detail="Provide 1-10 URLs")
    
    results = []
    for url in urls:
        if not re.match(r"^https?://", url):
            url = f"https://{url}"
        results.append(mock_extract_metadata(url))
    
    return {"results": results}


try:
    from mangum import Mangum
    handler = Mangum(app, lifespan="off")
except ImportError:
    pass
