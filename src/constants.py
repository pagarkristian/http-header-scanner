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
    }
}

HEADER_WEIGHTS = {
    "Content-Security-Policy": 30,
    "Strict-Transport-Security": 25,
    "Permissions-Policy": 15,
    "X-Frame-Options": 10,
    "X-Content-Type-Options": 10,
    "Referrer-Policy": 10,
}
