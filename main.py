import subprocess
from pathlib import Path
import pprint

IGNORES = [
    'node_modules',
    'webpack',
    '__pycache__',
    '\\.next',
    '\\.astro',
    # '\\.venv'
]

def list_git_projects(root_path: Path) -> "list[Path]":
    # 指定したパスの中にあるgit管理されたディレクトリをリストアップする
    # TODO: 実装する
    return []

# git管理下のプロジェクトパスを受け取り、重要そうなファイルをリストする
def list_remained_files(project_path: Path) -> "list[Path]":
    grep_cmd = f"grep -v -e {' -e '.join(IGNORES)}"
    print(grep_cmd)
    result = subprocess.run(
        f"git ls-files --other --ignored --exclude-standard | {grep_cmd} ",
        shell=True,
        cwd=project_path,
        capture_output=True
    )
    path_str_list = result.stdout.decode().split("\n")
    # TODO: シンボリックリンクでプロジェクト外を見ているのを削除する
    return [ (project_path / Path(p)).resolve() for p in path_str_list if len(p) > 0 ]

if __name__ == "__main__":
    pprint.pp(list_remained_files(Path("./")))
