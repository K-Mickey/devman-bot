from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    bot_token: str
    restart_delay: int = 60
    devman_token: str

    admin_id: str
    log_level: str = 'INFO'
    log_format: str = '[%(asctime)s] [%(levelname)s] [%(name)s - %(filename)s] > %(lineno)d - %(message)s'

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
