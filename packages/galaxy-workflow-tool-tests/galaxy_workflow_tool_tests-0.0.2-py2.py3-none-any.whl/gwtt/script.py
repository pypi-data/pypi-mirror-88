"""Entry point for galaxy-workflow-tool-tests."""
import sys

from bioblend import galaxy
from galaxy.tool_util.verify.script import (
    arg_parser,
    run_tests,
)

SCRIPT_DESCRIPTION = """
Script to run all the tool tests for all the tools in a Galaxy workflow.
"""


def main(argv=None):
    """Entry point function for galaxy-workflow-tool-tests."""
    if argv is None:
        argv = sys.argv[1:]

    parser = arg_parser()
    parser.add_argument('workflow_id', metavar='WORKFLOW_ID',
                        help='workflow id to scan for tools')
    args = parser.parse_args(argv)
    gi = galaxy.GalaxyInstance(url=args.galaxy_url, key=args.admin_key or args.key)
    workflows = gi.workflows
    workflow_dict = workflows.export_workflow_dict(args.workflow_id)
    tool_ids = []
    for step_dict in workflow_dict.get("steps").values():
        if not step_dict.get("type") == "tool":
            continue
        tool_ids.append(step_dict["tool_id"])

    def tool_not_in_workflow(test_reference):
        return test_reference.tool_id not in tool_ids

    run_tests(args, test_filters=[tool_not_in_workflow])


__all__ = (
    'main',
)
