from pathlib import Path
import git

config_dir = Path.home() / '.gnote'
config_dir.mkdir(parents=True, exist_ok=True)

repo_dir = config_dir / 'repo'
repo_url = 'git@gitee.com:gitgj/code-notes.git'


def __init_repo():
    if (repo_dir / '.git').exists():  # 当本地仓库存在时，拉取更新
        git_local = git.Repo(repo_dir)
        git_remote = git_local.remote()
        git_remote.pull()
    else:  # 当本地仓库不存在时，clone repository
        git_local = git.Repo.clone_from(url=repo_url, to_path=repo_dir, multi_options=['--depth 1'])
        git_local.config_writer().set_value('user', 'name', 'guojian').release()
        git_local.config_writer().set_value('user', 'email', 'guojian_k@qq.com').release()
    return git_local


git_repo = __init_repo()
