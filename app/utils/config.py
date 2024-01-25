from pydantic import BaseSettings, Field

class EnvVars(BaseSettings):
    MYSQL_URL: str = Field(default="", env="MYSQL_URL")
    REDIS_HOST: str = Field(default="", env="REDIS_HOST")
    REDIS_PORT: str = Field(default="", env="REDIS_PORT")
    FRONT_URL: str = Field(default="", env="FRONT_URL")

settings: EnvVars = EnvVars()

