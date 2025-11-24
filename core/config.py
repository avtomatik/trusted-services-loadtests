import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    DB_USER: str = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD: str = os.getenv('DB_PASSWORD', 'default_pass')
    DB_HOST: str = os.getenv('DB_HOST', 'localhost')
    DB_PORT: str = os.getenv('DB_PORT', '5432')
    DB_NAME: str = os.getenv('DB_NAME', 'default_db_name')

    MQ_USER: str = os.getenv('MQ_USER', 'guest')
    MQ_PASSWORD: str = os.getenv('MQ_PASSWORD', 'guest')
    MQ_HOST: str = os.getenv('MQ_HOST', 'localhost')
    MQ_PORT: str = os.getenv('MQ_PORT', '5672')

    REDIS_HOST: str = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT: str = os.getenv('REDIS_PORT', '6379')
    REDIS_DB: str = os.getenv('REDIS_DB', '0')

    @property
    def db_dsn(self) -> str:
        return (
            f'postgresql://{self.DB_USER}:{self.DB_PASSWORD}@'
            f'{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
        )

    @property
    def mq_url(self) -> str:
        return (
            f'amqp://{self.MQ_USER}:{self.MQ_PASSWORD}'
            f'@{self.MQ_HOST}:{self.MQ_PORT}/'
        )

    @property
    def redis_url(self) -> str:
        return f'redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}'


settings = Settings()
