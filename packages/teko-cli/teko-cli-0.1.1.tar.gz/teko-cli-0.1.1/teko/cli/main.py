import typer

from teko.cli import jira_command, cs_command

app = typer.Typer()
app.add_typer(jira_command.app, name="jira")
app.add_typer(cs_command.app, name="cs")

if __name__ == "__main__":
    app()
