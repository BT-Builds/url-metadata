# URL Metadata Extractor API

Extract titles, descriptions, images, and Open Graph metadata from any URL.

## Endpoints

### GET /health
Health check endpoint (no auth required)

### POST /extract
Extract metadata from a single URL

```bash
curl -X POST https://{slug}.vercel.app/extract \
  -H "Content-Type: application/json" \
  -H "api_key: demo-key" \
  -d '{"url": "https://example.com"}'
```

### POST /bulk
Extract metadata from up to 10 URLs

```bash
curl -X POST https://{slug}.vercel.app/bulk \
  -H "Content-Type: application/json" \
  -H "api_key: demo-key" \
  -d '{"urls": ["https://example.com", "https://github.com"]}'
```

## Response Format

```json
{
  "url": "https://example.com",
  "domain": "example.com",
  "title": "Example Domain",
  "description": "This is an example domain",
  "image": "https://example.com/og.png",
  "site_name": "Example",
  "favicon": "https://example.com/favicon.ico"
}
```

## Pricing
- Free: 100 requests/hour
- Pro: $29/month - 10,000 requests/hour, custom timeouts

## Monetization
List on RapidAPI for $15/month team plan.
