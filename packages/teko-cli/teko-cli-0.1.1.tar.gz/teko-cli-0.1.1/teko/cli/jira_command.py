from pathlib import Path

import typer
from teko.services.jira.jira_service import JiraService

app = typer.Typer()


@app.command(name="create-tests")
def create_testcases(
        file: str = typer.Argument(..., help='The name of a testcase definition file'),
   ):
    """
    """
    print("Jira create tests")
    jira_srv = JiraService()
    testcases = jira_srv.read_testcases_from_file(file)
    jira_srv.create_or_update_testcases_by_name(testcases)


@app.command(name="create-cycle")
def create_test_cycles(
        file: str = typer.Argument(..., help='The name of a testcase result file'),
   ):
    """
    """
    print("Jira submit test")
    jira_srv = JiraService()
    testcases = jira_srv.read_testcases_from_file(file)
    jira_srv.create_test_cycle(testcases)
