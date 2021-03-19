from invoke import task


@task
def set_up_git_hooks(c):
    """Set up predefined hooks to the project's GIT repo."""
    c.run('git config core.hooksPath git-hooks')
    c.run('chmod +x git-hooks/*')


@task
def pep8(c, path=''):
    """Check files in path by PEP8 standard."""
    c.run(f'flake8 {path}')


@task
def order_imports(c, path=''):
    """Order imports by isort."""
    c.run(f'isort {path}')


@task
def check_code_style(c, path=''):
    """Order imports by isort and check files by PEP8 standard."""
    order_imports(c, path)
    pep8(c, path)
