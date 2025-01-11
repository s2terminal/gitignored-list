from pathlib import Path
import pprint
from typing import Tuple, Type

from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    YamlConfigSettingsSource,
    CliApp
)

from src.gitignored_list.run_cmd import list_git_projects, list_remained_files

class Settings(BaseSettings):
    model_config = SettingsConfigDict(yaml_file='config.yaml')

    unnecessaries: "list[str]"
    path: str

    def cli_cmd(self) -> None:
        for project in list_git_projects(Path(self.path)):
            print("##", project)
            pprint.pp(
                list_remained_files(project, unnecessaries=self.unnecessaries)
            )

    # https://docs.pydantic.dev/latest/concepts/pydantic_settings/#other-settings-source
    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (YamlConfigSettingsSource(settings_cls),)

if __name__ == "__main__":
    CliApp.run(Settings)
