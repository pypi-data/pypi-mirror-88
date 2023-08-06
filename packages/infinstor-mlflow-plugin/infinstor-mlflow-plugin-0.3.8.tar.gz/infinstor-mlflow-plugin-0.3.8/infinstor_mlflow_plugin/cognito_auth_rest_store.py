from mlflow.store.tracking.rest_store import RestStore
from mlflow.utils.rest_utils import MlflowHostCreds
from infinstor_mlflow_plugin.tokenfile import get_token
from os.path import expanduser
from os.path import sep as separator
from mlflow.entities import (
        ViewType
        )

class CognitoAuthenticatedRestStore(RestStore):
    def cognito_host_creds(self):
        tokfile = expanduser("~") + separator + '.infinstor' + separator + 'token'
        token, service = get_token(tokfile, False)
        return MlflowHostCreds('https://mlflow.' + service + '.com:443/', token=token)

    def get_service(self):
        tokfile = expanduser("~") + separator + '.infinstor' + separator + 'token'
        token, service = get_token(tokfile, False)
        return service

    def get_token_string(self):
        tokfile = expanduser("~") + separator + '.infinstor' + separator + 'token'
        token, service = get_token(tokfile, False)
        return token

    def _hard_delete_run(self, run_id):
        """
        Permanently delete a run (metadata and metrics, tags, parameters).
        This is used by the ``mlflow gc`` command line and is not intended to be used elsewhere.
        """
        print('_hard_delete_run: Entered. run_id=' + str(run_id))
        return

    def _get_deleted_runs(self):
        print('_get_deleted_runs: Entered')
        experiments = self.list_experiments(view_type=ViewType.ALL)
        experiment_ids = map(lambda x: x.experiment_id, experiments)
        print('_get_deleted_runs: experiment_ids=' + str(experiment_ids))
        deleted_runs = self.search_runs(
            experiment_ids=experiment_ids, filter_string="", run_view_type=ViewType.DELETED_ONLY
        )
        rv = [deleted_run.info.run_uuid for deleted_run in deleted_runs]
        print('_get_deleted_runs: deleted_runs=' + str(rv))
        return rv


    def __init__(self, store_uri=None, artifact_uri=None):
        super().__init__(self.cognito_host_creds)

