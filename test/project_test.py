from pathlib import Path
import pytest
from src.gitignored_list.project import Project

def test_project():
    pj = Project(path=Path("./"), name="src")
    assert pj.name == "src"

def test_project_path_not_exist():
    with pytest.raises(Exception):
        Project(path=Path("not_exist_path"), name="src")

def test_to_projects():
    projects = Project.to_projects(
        root_path=Path("./"),
        pj_path_list=["src", ""]
    )
    assert len(projects) == 1
    assert projects[0] == Project(path=Path("./src"), name="src")

def test_not_exist_project():
    with pytest.raises(Exception):
        Project.to_projects(
            root_path=Path("./"),
            pj_path_list=["not_exist_path", ""]
        )

def test_hold_path():
    pj = Project(path=Path("./src"), name="src")
    hold_path_list = pj.hold_path_list(["gitignored_list/project.py"])
    assert len(hold_path_list) == 1
    assert hold_path_list[0] == Path("./gitignored_list/project.py")
    # project_path / hold_file が存在すること
    assert (pj.path / hold_path_list[0]).exists()
    # save_path / project_name / hold_file が作れること（作成するため、存在しなくてOK）
    save_path = Path("save_path")
    assert save_path / Path(pj.name) / hold_path_list[0] == Path("save_path/src/gitignored_list/project.py")

def test_not_exist_hold_path():
    pj = Project(path=Path("./src"), name="src")
    hold_path_list = pj.hold_path_list(["not_exist_path/project.py"])
    assert len(hold_path_list) == 0
