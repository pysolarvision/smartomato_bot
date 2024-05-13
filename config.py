from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from pathlib import Path


class Config(BaseSettings):
    path_load: Path = Field(..., env='PATH_LOAD')
    path_upload_v1: Path = Field(Path('data/changed_groups/v1'), env='PATH_UPLOAD_V1')
    path_upload_v2: Path = Field(Path('data/changed_groups/v2'), env='PATH_UPLOAD_V2')
    bot_token: str = Field(..., env='BOT_TOKEN')

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
