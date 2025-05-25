class Settings():
    MONGO_URI: str = "mongodb://mongo:27017"
    MONGO_DB: str = "test_db"
    COLLECTION_NAME: str = "otziv_collection"
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    class Config:
        env_file = ".env"

settings = Settings()