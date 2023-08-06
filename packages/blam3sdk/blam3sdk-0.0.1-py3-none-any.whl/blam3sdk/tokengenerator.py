from blam3sdk.blam.enums import AuthorisationLevel
import jwt
import uuid

from datetime import datetime, timedelta

class TokenGenerator():
    def __init__(self, secret: str):
        self._secret = secret

    def generateToken(self, orgId: int) -> str:

        now = datetime.utcnow() + timedelta(seconds=-30)

        claims = {
            "jti": f'{uuid.uuid4()}',
            "iat": now.strftime(r'%d/%m/%Y %H:%M:%S'),
            "nbf": now,
            "exp": now + timedelta(days=28),
            "iss": "BLAM",
            "aud": "ApiUser",
            "name": "Workflow Agent",
            "http://schemas.microsoft.com/ws/2008/06/identity/claims/userdata": '0',
            "organisation": orgId,
            "authorisationLevel": AuthorisationLevel.workflow.name.title(),
            "runNodeId": 0,
            "workflowRunId": 0,
            "permissions": self.permissions
        }

        return jwt.encode(claims, self._secret.encode('ascii'), algorithm='HS256').decode("utf-8")

    @property
    def permissions(self):
        return ["ViewAssets",
            "CreateAssets",
            "ModifyAssets",
            "DeleteAssets",
            "ViewFileStores",
            "CreateFileStores",
            "ModifyFileStores",
            "DeleteFileStores",
            "ViewCredentials",
            "CreateCredentials",
            "ModifyCredentials",
            "DeleteCredentials",
            "ViewUsers",
            "CreateUsers",
            "ModifyUsers",
            "DeleteUsers",
            "ViewGroups",
            "CreateGroups",
            "ModifyGroups",
            "DeleteGroups",
            "ViewFolders",
            "CreateFolders",
            "ModifyFolders",
            "DeleteFolders",
            "ViewTasks",
            "CreateTasks",
            "ModifyTasks",
            "DeleteTasks",
            "ViewConfigurations",
            "CreateConfigurations",
            "ModifyConfigurations",
            "DeleteConfigurations",
            "ViewMetadata",
            "CreateMetadata",
            "ModifyMetadata",
            "DeleteMetadata",
            "ViewWatchfolders",
            "CreateWatchfolders",
            "ModifyWatchfolders",
            "DeleteWatchfolders",
            "ViewTriggers",
            "CreateTriggers",
            "ModifyTriggers",
            "DeleteTriggers",
            "ViewWorkflows",
            "CreateWorkflows",
            "ModifyWorkflows",
            "DeleteWorkflows",
            "ViewScheduledRecordings",
            "CreateScheduledRecordings",
            "ModifyScheduledRecordings",
            "DeleteScheduledRecordings",
            "ViewCostTracking",
            "CreateCostTracking",
            "ModifyCostTracking",
            "DeleteCostTracking",
            "ViewWorkOrders",
            "CreateWorkOrders",
            "ModifyWorkOrders",
            "DeleteWorkOrders"]
