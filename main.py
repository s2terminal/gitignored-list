from pathlib import Path
import os
import shutil
from typing import Tuple, Type, Optional

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
    copy_path: Optional[str] = None

    def cli_cmd(self) -> None:
        if self.copy_path is not None:
            os.mkdir(self.copy_path) # 存在していたら例外
        for pj in list_git_projects(Path(self.path)):
            print("##", pj)
            for hold_file in list_hold_files(pj, unnecessaries=self.unnecessaries):
                copy_from_path = pj.path / hold_file
                if self.copy_path is not None:
                    copy_to_path = Path(self.copy_path) / pj.name / hold_file
                    os.makedirs(copy_to_path.parent, exist_ok=True) # 再帰的に作成、存在していてもOK
                    shutil.copy(copy_from_path, copy_to_path)
                else:
                    print(os.path.getsize(copy_from_path), hold_file)

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
