"""
Setup script for the GRC platform backend.
"""

from setuptools import setup, find_packages

setup(
    name="grc-platform-backend",
    version="1.0.0",
    description="GRC Platform Backend Services",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "fastapi>=0.68.0",
        "uvicorn>=0.15.0",
        "psycopg2-binary>=2.9.0",
        "redis>=4.0.0",
        "numpy>=1.21.0",
        "pydantic>=1.8.0",
        "python-jose[cryptography]>=3.3.0",
        "passlib[bcrypt]>=1.7.4",
        "python-multipart>=0.0.5",
        "sqlalchemy>=1.4.0",
        "alembic>=1.7.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-asyncio>=0.15.0",
            "black>=21.0.0",
            "flake8>=3.9.0",
            "mypy>=0.910",
        ]
    },
)

