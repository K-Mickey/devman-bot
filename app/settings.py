from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    bot_token: str
    devman_token: str

    log_level: str = 'INFO'
    log_format: str = '[%(asctime)s] [%(levelname)s] [%(name)s - %(filename)s] > %(lineno)d - %(message)s'

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
