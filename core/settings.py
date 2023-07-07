from pydantic import BaseSettings


class Settings(BaseSettings):
    PROVIDER_URL: str = "https://rpc-mumbai.maticvigil.com"
    PRIVATE_KEY: str
    RECEIVER_ADDRESS: str = "0x4Ba760E5361cf7c9031698ea6dF979a9e989e869"

    class Config:
        env_file = ".env"


settings = Settings()
