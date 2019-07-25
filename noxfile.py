import nox

files = ["asyncnostic", "tests", "noxfile.py"]


@nox.session(python=["3.7"])
def tests(session):
    """Run test suite with pytest"""
    session.install("-r", "requirements.txt")
    session.run("pytest")


@nox.session(python=["3.7"])
def blacken(session):
    """Run black code formater."""
    session.install("black")
    session.run("black", *files)


@nox.session(python="3.7")
def lint(session):
    """Lint using flake8."""
    session.install("flake8", "black")
    session.run("black", "--check", *files)
    session.run("flake8", *files)
