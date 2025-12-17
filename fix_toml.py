import tomli_w

config = {
    "tool": {
        "poetry": {
            "name": "project#2-baikov-maksim-m25-555",
            "version": "0.1.0",
            "description": "",
            "authors": ["lYoungunl <max10129595@mail.ru>"],
            "readme": "README.md",
            "packages": [{"include": "src"}],
            "dependencies": {
                "python": "^3.13",
                "prompt": "^0.4.1"
            },
            "group": {
                "dev": {
                    "dependencies": {
                        "ruff": "^0.14.9"
                    }
                }
            },
            "scripts": {
                "project": "src.primitive_db.main:main"
            }
        },
        "ruff": {
            "line-length": 88,
            "target-version": "py312",
            "exclude": ["venv", ".venv", "dist", "__pycache__"],
            "lint": {
                "select": ["E", "F", "I"],
                "ignore": []
            },
            "format": {
                "quote-style": "double"
            }
        }
    },
    "build-system": {
        "requires": ["poetry-core"],
        "build-backend": "poetry.core.masonry.api"
    }
}

with open("pyproject.toml", "w", encoding="utf-8") as f:
    tomli_w.dump(config, f)
