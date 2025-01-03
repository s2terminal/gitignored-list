import subprocess
import pathlib
import pprint

IGNORES = [
    'node_modules',
    'webpack',
    '__pycache__',
    '\\.next',
    '\\.astro',
    # '\\.venv'
]

def list_git_projects(root_path: pathlib.Path) -> "list[str]":
    # 指定したパスの中にあるgit管理されたディレクトリをリストアップする
    # TODO: 実装する
    pass

# git管理下のプロジェクトパスを受け取り、重要そうなファイルをリストする
def list_remained_files(project_path: pathlib.Path) -> "list[str]":
    grep_cmd = f"grep -v -e {' -e '.join(IGNORES)}"
    print(grep_cmd)
    result = subprocess.run(
        f"git ls-files --other --ignored --exclude-standard | {grep_cmd} ",
        shell=True,
        cwd=project_path,
        capture_output=True
    )
    # TODO: 絶対パスにする
    return [ p for p in result.stdout.decode().split("\n") if len(p) > 0 ]

if __name__ == "__main__":
    pprint.pp(list_remained_files(pathlib.Path("./")))
