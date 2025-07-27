# Security Configuration Summary

## HTTPS Enforcement
- `SECURE_SSL_REDIRECT = True`: Forces HTTPS across the entire site.
- `SECURE_HSTS_SECONDS = 31536000`: Instructs browsers to enforce HTTPS for 1 year.
- `SECURE_HSTS_INCLUDE_SUBDOMAINS = True`: HSTS applies to subdomains.
- `SECURE_HSTS_PRELOAD = True`: Enables HSTS preload for browser-level enforcement.

## Secure Cookies
- `SESSION_COOKIE_SECURE = True`: Session cookies sent only over HTTPS.
- `CSRF_COOKIE_SECURE = True`: CSRF cookies sent only over HTTPS.

## Secure Headers
- `X_FRAME_OPTIONS = "DENY"`: Prevents site from being embedded in iframes.
- `SECURE_CONTENT_TYPE_NOSNIFF = True`: Prevents MIME-type sniffing.
- `SECURE_BROWSER_XSS_FILTER = True`: Enables browser-based XSS protection.

## Deployment Notes
- SSL configured with Let's Encrypt.
- Redirects all HTTP traffic to HTTPS using Nginx.

## Recommendations
- Consider setting a Content Security Policy (CSP) using `django-csp`.
- Regularly review Django's [deployment checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/).
