import os

import nox


def is_in_ci():
    return os.getenv('CI') == 'true'


def install_dependencies(session, group):
    session.install('poetry')
    if is_in_ci():
        session.run('poetry', 'config', 'virtualenvs.create', 'false')
    session.run('poetry', 'install', '--with', group)


@nox.session
def unit_tests(session):
    install_dependencies(session, 'test')
    # Generate coverage report for Codecov
    session.run(
        'poetry',
        'run',
        'pytest',
        '--cov=pythoncv',
        '--cov-report=term-missing',
        '--cov-report=xml',
    )


@nox.session
def coverage(session):
    session.install('coverage', 'codecov')
    session.run('coverage', 'xml')


@nox.session
def lint(session):
    session.install('toml', 'yapf', 'flake8', 'pyproject-flake8')
    session.run('yapf', '--in-place', '--recursive', './pythoncv')
    session.run('flake8', 'pythoncv')
    session.notify('mypy')


@nox.session
def mypy(session):
    install_dependencies(session, 'test')
    session.run('poetry', 'run', 'mypy', 'pythoncv')


@nox.session
def build_docs(session):
    session.install('poetry', 'pdoc')
    session.run('poetry', 'install')
    session.run('poetry', 'run', 'pdoc', '--no-show-source', '--output-dir', 'docs', '-d', 'google', '--math',
                'pythoncv')
