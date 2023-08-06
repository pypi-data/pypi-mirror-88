import platform
import subprocess
from enum import auto, Enum
from pathlib import Path

import click
import rich
from rich.markdown import Markdown

import gnote


class Opt(Enum):
    default = auto()
    version = auto()
    list = auto()
    edit = auto()


def __call_pyvim(doc_path):
    cmd = ['powershell'] if 'windows' == platform.system().lower() else []
    subprocess.call(cmd + ['pyvim', doc_path])


def __check_and_sync():
    g = gnote.git_repo
    if g.is_dirty(untracked_files=True):
        g.git.add('.')
        g.git.commit(m='update')
        g.git.push()


def edit_doc(words: str):
    if words is None: return
    if words.isspace(): return
    repo_path = gnote.repo_dir
    base_path = words + '.md'
    file_path = repo_path / base_path
    file_path.parent.mkdir(parents=True, exist_ok=True)
    __call_pyvim(file_path)
    __check_and_sync()


def list_dir(pwd_path: Path, parents: list, ans: list):
    for child in pwd_path.iterdir():
        if child.name.startswith('.'): continue
        if child.is_dir():
            parents.append(child.name)
            list_dir(child, parents, ans)
            parents.pop()
        else:  # 如果是文件
            parents.append(child.name.removesuffix('.md'))
            ans.append('/'.join(parents))
            parents.pop()


def list_docs():
    repo_path = gnote.repo_dir

    ans = []
    list_dir(repo_path, [], ans)

    for doc in ans:
        print(doc)


def show_doc(words: str):
    if words is None: return
    if words.isspace(): return
    repo_path = gnote.repo_dir
    base_path = words + '.md'
    file_path = repo_path / base_path
    if file_path.is_file():
        content = file_path.read_text()
        rich.print(Markdown(content))
    else:
        print(f"{words} is not exist")


@click.command()
@click.argument('words', nargs=1, required=False)
@click.option('-v', '--version', 'opt', flag_value=Opt.version)
@click.option('-l', '--list', 'opt', flag_value=Opt.list)
@click.option('-e', '--edit', 'opt', flag_value=Opt.edit)
def entry(words, opt):
    if opt is None:
        show_doc(words)
    else:
        if opt == Opt.version:
            print('0.3.2')
        if opt == Opt.list:
            list_docs()
        if opt == Opt.edit:
            edit_doc(words)
