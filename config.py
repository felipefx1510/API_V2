import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///tasks.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
