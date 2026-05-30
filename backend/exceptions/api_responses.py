"""
OpenAPI response schemas for Swagger documentation.
"""

API_RESPONSES = {
    400: {
        "description": "Bad Request",
        "content": {"application/json": {"example": {"detail": "Invalid data"}}},
    },
    401: {
        "description": "Unauthorized",
        "content": {
            "application/json": {"example": {"detail": "Authentication required"}}
        },
    },
    403: {
        "description": "Forbidden",
        "content": {"application/json": {"example": {"detail": "Permission denied"}}},
    },
    404: {
        "description": "Not Found",
        "content": {"application/json": {"example": {"detail": "Resource not found"}}},
    },
    409: {
        "description": "Conflict",
        "content": {
            "application/json": {"example": {"detail": "Resource already exists"}}
        },
    },
    422: {
        "description": "Validation Error",
        "content": {
            "application/json": {
                "example": {
                    "detail": "email: Invalid email format; password: String should have at least 8 characters",
                    "message_key": "validation_error",
                    "errors": [
                        {
                            "field": "email",
                            "message": "Invalid email format",
                            "message_key": "validation.value_error",
                            "params": {"field": "email"},
                        },
                        {
                            "field": "password",
                            "message": "String should have at least 8 characters",
                            "message_key": "validation.string_too_short",
                            "params": {"field": "password", "min_length": 8},
                        },
                    ],
                }
            }
        },
    },
    500: {
        "description": "Internal Server Error",
        "content": {
            "application/json": {"example": {"detail": "An unexpected error occurred"}}
        },
    },
}
