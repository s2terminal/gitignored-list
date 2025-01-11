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
