import subprocess
from pathlib import Path
from .logger import logger
from .project import Project

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
    return Project.to_projects(root_path, project_path_list)

def list_hold_files(project: Project, unnecessaries: "list[str]") -> "list[Path]":
    """
    git管理プロジェクトを受け取り、重要そうなファイルをリストする
    プロジェクトパスからの相対パスのリストを返す
    """
    grep_cmd = f"grep -v -e {' -e '.join(unnecessaries)}"
    path_str_list = _run_cmd(
        command=f"git ls-files --other --ignored --exclude-standard | {grep_cmd} ",
        workdir=project.path
    ).split("\n")
    return project.hold_path_list(path_str_list)
