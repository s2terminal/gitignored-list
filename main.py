import subprocess
from pathlib import Path
import pprint
from typing import Tuple, Type

from pydantic import BaseModel
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    YamlConfigSettingsSource,
    CliApp
)

import sys
import logging

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
logger.setLevel(logging.INFO)
handler.setLevel(logging.INFO)
logger.addHandler(handler)

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

class Project(BaseModel):
    """
    self.path Path:
        コマンド実行時の解決可能なパス
    self.name str:
        保存先のパスとして使う名前
    """
    path: Path
    name: str

    def __init__(self, **data):
        super().__init__(**data)
        self.validate_path()

    def validate_path(self):
        if not self.path.exists():
            raise Exception("存在しないパスです", self.path)

def _run_cmd(command: str, workdir: Path) -> str:
    logger.debug(command)
    result = subprocess.run(command, shell=True, cwd=workdir, capture_output=True)
    return result.stdout.decode()

def list_git_projects(root_path: Path) -> "list[Project]":
    """
    指定したパスの中にあるgit管理プロジェクトをリストアップする
    """
    project_path_list = _run_cmd(
        'find ./ -name ".git" -type d -print0 | xargs -0 -I {} dirname {}',
        root_path
    ).split("\n")
    return [ Project(path=( root_path / Path(p)), name=p) for p in project_path_list if len(p) > 0 ]

def list_remained_files(project: Project, unnecessaries: "list[str]") -> "list[Path]":
    """
    git管理プロジェクトを受け取り、重要そうなファイルをリストする
    プロジェクトパスからの相対パスのリストを返す
    """
    grep_cmd = f"grep -v -e {' -e '.join(unnecessaries)}"
    path_str_list = _run_cmd(
        command=f"git ls-files --other --ignored --exclude-standard | {grep_cmd} ",
        workdir=project.path
    ).split("\n")
    # TODO: シンボリックリンクでプロジェクト外を見ているのを削除する
    path_list = [ (project.path / Path(p)) for p in path_str_list if len(p) > 0 ]
    return list(filter(lambda p: p.exists(), path_list))

if __name__ == "__main__":
    CliApp.run(Settings)
