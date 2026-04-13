from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./brajpath.db"
    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_WHATSAPP_FROM: str = "whatsapp:+14155238886"
    PUBLIC_WEBHOOK_BASE_URL: str = ""
    ADMIN_WA_NUMBER: str = ""
    APP_ENV: str = "development"
    APP_TIMEZONE: str = "Asia/Kolkata"
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
