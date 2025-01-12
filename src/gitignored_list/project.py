from pathlib import Path
from pydantic import BaseModel

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

    def hold_path_list(self, path_str_list: list[str]) -> list[Path]:
        """
        プロジェクトの管理下にある重要そうなファイル一覧を受け取って、pj.pathからのコピー可能なリストにして返す
        """
        # TODO: シンボリックリンクでプロジェクト外を見ているのを削除する
        path_list = [ Path(p) for p in path_str_list if len(p) > 0 ]
        return list(filter(lambda p: (self.path / p).exists(), path_list))

    @classmethod
    def to_projects(cls, root_path: Path, pj_path_list: list[str]) -> "list[Project]":
        """
        git管理下のプロジェクトへのパスの文字列を受け取って、プロジェクトオブジェクトを返す
        """
        return [ cls(path=( root_path / Path(p)), name=p) for p in pj_path_list if len(p) > 0 ]
