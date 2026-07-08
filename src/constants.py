"""
Project constants
"""

SECURITY_HEADERS=[
    "Content-Security-Policy",
    "Strict-Transport-Security",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Referrer-Policy",
    "Permissions-Policy",
    "Cross-Origin-Opener-Policy",
    "Cross-Origin-Embedder-Policy",
    "Cross-Origin-Resource-Policy",
    "X-Permitted-Cross-Domain-Policies",
]

HEADER_INFORMATION = {
    "Content-Security-Policy": {
        "risk": "Helps prevent Cross-Site Scripting (XSS) attacks.",
        "recommendation": "Configure the Content-Security-Policy header."
    },

    "Strict-Transport-Security": {
        "risk": "HTTPS is not enforced for future connections.",
        "recommendation": "Add: Strict-Transport-Security: max-age=31536000"
    },

    "X-Frame-Options": {
        "risk": "Missing protection against clickjacking attacks.",
        "recommendation": "Set: X-Frame-Options: SAMEORIGIN"
    },

    "X-Content-Type-Options": {
        "risk": "Browsers may MIME-sniff files.",
        "recommendation": "Set: X-Content-Type-Options: nosniff"
    },

    "Referrer-Policy": {
        "risk": "Sensitive URL information may leak.",
        "recommendation": "Set an appropriate Referrer-Policy."
    },

    "Permissions-Policy": {
        "risk": "Browser features are not restricted.",
        "recommendation": "Define a Permissions-Policy header."
    },

    "Cross-Origin-Opener-Policy": {
        "risk": "Other origins may keep a window reference to this page, enabling cross-window attacks (e.g. Spectre-style side channels).",
        "recommendation": "Set: Cross-Origin-Opener-Policy: same-origin"
    },

    "Cross-Origin-Embedder-Policy": {
        "risk": "This page can load cross-origin resources without their explicit consent, weakening cross-origin isolation.",
        "recommendation": "Set: Cross-Origin-Embedder-Policy: require-corp"
    },

    "Cross-Origin-Resource-Policy": {
        "risk": "Other websites may embed or load this site's resources (images, scripts, etc.) without restriction.",
        "recommendation": "Set: Cross-Origin-Resource-Policy: same-origin"
    },

    "X-Permitted-Cross-Domain-Policies": {
        "risk": "Legacy plugins (e.g. Flash, Acrobat) may be allowed to make cross-domain requests to this site.",
        "recommendation": "Set: X-Permitted-Cross-Domain-Policies: none"
    }
}

HEADER_WEIGHTS = {
    "Content-Security-Policy": 25,
    "Strict-Transport-Security": 20,
    "Permissions-Policy": 12,
    "X-Frame-Options": 8,
    "X-Content-Type-Options": 8,
    "Referrer-Policy": 8,
    "Cross-Origin-Opener-Policy": 7,
    "Cross-Origin-Resource-Policy": 5,
    "Cross-Origin-Embedder-Policy": 5,
    "X-Permitted-Cross-Domain-Policies": 2,
}
