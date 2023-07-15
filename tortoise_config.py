TORTOISE_ORM = {
    "connections": {
        "default": "sqlite://:memory:",
    },
    "apps": {
        "models": {
            "models": ["main"],
            "default_connection": "default",
        },
    },
}
