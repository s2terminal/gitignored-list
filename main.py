from pathlib import Path
from os.path import getsize
from typing import Tuple, Type

from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    YamlConfigSettingsSource,
    CliApp
)

from src.gitignored_list.run_cmd import list_git_projects, list_hold_files

class Settings(BaseSettings):
    model_config = SettingsConfigDict(yaml_file='config.yaml')

    unnecessaries: "list[str]"
    path: str

    def cli_cmd(self) -> None:
        for project in list_git_projects(Path(self.path)):
            print("##", project)
            for hold_file in list_hold_files(project, unnecessaries=self.unnecessaries):
                print(getsize(project.path / hold_file), hold_file)

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
