import subprocess
from pathlib import Path
import pprint

import yaml
from pydantic_settings import BaseSettings

import sys
import logging

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
logger.setLevel(logging.INFO)
handler.setLevel(logging.INFO)
logger.addHandler(handler)

class Settings(BaseSettings):
    unnecessaries: "list[str]"
    base_path: str

def _run_cmd(command: str, workdir: Path) -> str:
    logger.debug(command)
    result = subprocess.run(command, shell=True, cwd=workdir, capture_output=True)
    return result.stdout.decode()

def list_git_projects(root_path: Path) -> "list[Path]":
    # 指定したパスの中にあるgit管理されたディレクトリをリストアップする
    project_path_list = _run_cmd(
        'find ./ -name ".git" -type d -print0 | xargs -0 -I {} dirname {}',
        root_path
    ).split("\n")
    return [ (root_path / Path(p)).resolve() for p in project_path_list if len(p) > 0 ]

# git管理下のプロジェクトパスを受け取り、重要そうなファイルをリストする
def list_remained_files(project_path: Path, unnecessaries: "list[str]") -> "list[Path]":
    grep_cmd = f"grep -v -e {' -e '.join(unnecessaries)}"
    path_str_list = _run_cmd(
        command=f"git ls-files --other --ignored --exclude-standard | {grep_cmd} ",
        workdir=project_path
    ).split("\n")
    # TODO: シンボリックリンクでプロジェクト外を見ているのを削除する
    return [ (project_path / Path(p)).resolve() for p in path_str_list if len(p) > 0 ]

if __name__ == "__main__":
    with open("config.yaml", "r") as file:
        settings = Settings(**yaml.safe_load(file))

    for project_path in list_git_projects(Path("../")):
        print("##", project_path)
        pprint.pp(
            list_remained_files(project_path, unnecessaries=settings.unnecessaries)
        )
