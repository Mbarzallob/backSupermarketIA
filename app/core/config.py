from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    VERTEX_LOCATION: str
    VERTEX_PROJECT_ID: str
    SUPABASE_KEY: str
    SUPABASE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()
