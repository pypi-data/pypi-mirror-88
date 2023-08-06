from __future__ import annotations

from typing import Any, List

from colorama import Fore

from baseten.common import api
from baseten.common.core import InvokingUnpublishedWorkflowError
from baseten.common.settings import API_URL_BASE
from baseten.common.util import print_error_response
from baseten.workflow.atom import RegisteredAtom
from baseten.workflow.query import Query
from baseten.workflow.worklet import Worklet


class Workflow:
    """Workflow is a meaningful flow of activities.

    Consists of worklets, their triggers and state.
    """

    def __init__(self, name: str):
        self._id = None
        self._name = name
        self._worklets = []
        self._queries = []

    def add_worklet(self, worklet: Worklet):
        self._worklets.append(worklet)

    def add_worklets(self, worklets: List[Worklet]):
        self._worklets.extend(worklets)

    def add_query(self, query: Query):
        self._queries.append(query)

    def add_queries(self, queries: List[Query]):
        self._queries.extend(queries)

    def publish(self):
        worklet_configs = [w.to_json() for w in self._worklets]
        query_configs = [q.to_json() for q in self._queries]
        response = api.update_or_create_workflow(self._name, worklet_configs, query_configs)
        self._id = response['id']
        print(Fore.GREEN + f'Published successfully. Visit: ' + Fore.WHITE + f'{API_URL_BASE}/workflows/{self._id}')

    def invoke_worklet(self,
                       worklet_name: str,
                       worklet_input,
                       create_workflow_instance=False,
                       dry_run=False,
                       print_response=True):
        if not self._id:
            raise InvokingUnpublishedWorkflowError('You must first publish the workflow before invoking its worklets.')

        response = api.invoke_worklet(self._id,
                                      worklet_name,
                                      worklet_input,
                                      create_workflow_instance,
                                      dry_run)

        if print_response:
            if not response['success']:
                print(Fore.RED + f'Invoking worklet "{worklet_name}" failed.')
                print_error_response(response)
            else:
                print(Fore.GREEN + f'Worklet {worklet_name} executed successfully with input:'
                      + Fore.WHITE + f' {worklet_input}')
                print(Fore.GREEN + f'Worklet Output:' + Fore.WHITE + f' {response["worklet_output"]}')
                if dry_run:
                    print(Fore.YELLOW + f'Execution Log:\n{response["execution_log"]}')

        return response

    def dryrun(self, reg_atom: RegisteredAtom, atom_input: Any):
        """
        Dryrun an atom.

        Dryrun happens on the backend where appropriate context is provided to the atom. Note
        that workflow_instance_id in the context will be none as that's not available at the
        atom level.
        Dryrun means that no state is implicitly persisted but Atom code may still create side
        effects. To guard against those, Atom code should use the dryrun flag which will be set
        to True for dry run but is False for regular execution.
        """
        name = reg_atom.name
        conf = reg_atom.conf
        response = api.dryrun_atom(name, conf, atom_input, self._name)
        if not response['success']:
            print(Fore.RED + f'Invoking atom "{name}" failed.')
            print_error_response(response)
        else:
            print(Fore.GREEN + f'Atom {name} executed successfully with input:'
                  + Fore.WHITE + f' {atom_input}')
            print(Fore.GREEN + f'Atom Output:' + Fore.WHITE + f' {response["atom_output"]}')
            print(Fore.YELLOW + f'Execution Log:\n{response["execution_log"]}')
        return response

    @classmethod
    def from_name(cls, workflow_name: str) -> Workflow:
        response = api.workflow(workflow_name)
        workflow = cls(workflow_name)
        workflow._id = response['id']
        return workflow
