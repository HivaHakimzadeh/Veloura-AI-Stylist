from setuptools import find_packages, setup


setup(
    name="veloura-backend",
    version="0.1.0",
    description="Backend for Veloura AI Stylist",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "alembic>=1.13.2",
        "boto3>=1.34.0",
        "celery[redis]>=5.4.0",
        "fastapi>=0.111.0",
        "httpx>=0.27.0",
        "openai>=1.35.0",
        "pillow>=10.4.0",
        "psycopg[binary]>=3.2.0",
        "pydantic-settings>=2.3.4",
        "python-multipart>=0.0.9",
        "redis>=5.0.7",
        "sqlalchemy>=2.0.31",
        "uvicorn[standard]>=0.30.1",
    ],
    extras_require={
        "dev": [
            "pytest>=8.2.2",
            "pytest-asyncio>=0.23.7",
            "pytest-cov>=5.0.0",
            "ruff>=0.5.0",
        ]
    },
)
