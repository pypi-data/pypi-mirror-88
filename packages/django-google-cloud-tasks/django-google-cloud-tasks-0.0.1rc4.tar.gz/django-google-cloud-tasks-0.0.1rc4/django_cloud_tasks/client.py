# pylint: disable=not-callable, unsubscriptable-object
import abc
import logging
import os
import uuid
from datetime import datetime, timedelta

from google import auth
from google.api_core.exceptions import NotFound, FailedPrecondition
from google.cloud import tasks_v2, scheduler
from google.protobuf import timestamp_pb2
from googleapiclient.discovery import build

logger = logging.getLogger(__name__)

DEFAULT_LOCATION = 'us-east1'
DEFAULT_TIMEZONE = 'UTC'
DEFAULT_PROJECT_ID = os.environ.get('PROJECT_ID')


class GoogleCloudPilotAPI(abc.ABC):
    _client_class = None
    _scopes = ['https://www.googleapis.com/auth/cloud-platform']

    def __init__(self, subject=None, **kwargs):
        self.credentials, project_id = self._build_credentials(subject=subject)

        self.project_id = kwargs.get('project') \
            or DEFAULT_PROJECT_ID \
            or getattr(self.credentials, 'project_id', project_id)

        self.client = (self._client_class or build)(
            credentials=self.credentials,
            **kwargs
        )

    @classmethod
    def _build_credentials(cls, subject=None):
        credentials, project_id = auth.default()

        if subject:
            credentials = credentials.with_subject(subject=subject)

        return credentials, project_id

    @property
    def oidc_token(self):
        return {'oidc_token': {'service_account_email': self.credentials.service_account_email}}


class CloudTasksClient(GoogleCloudPilotAPI):
    _client_class = tasks_v2.CloudTasksClient
    DEFAULT_METHOD = tasks_v2.HttpMethod.POST

    def push(self, name, queue, url, payload, method=DEFAULT_METHOD, delay_in_seconds=0, location=None, unique=True):
        parent = self.client.queue_path(
            project=self.project_id,
            location=location or DEFAULT_LOCATION,
            queue=queue,
        )
        if unique:
            name = f"{name}-{str(uuid.uuid4())}"

        task_name = self.client.task_path(
            project=self.project_id,
            location=location or DEFAULT_LOCATION,
            queue=queue,
            task=name,
        )
        task = tasks_v2.Task(
            name=task_name,
            http_request=tasks_v2.HttpRequest(
                http_method=method,
                url=url,
                body=payload.encode(),
                **self.oidc_token,
            )
        )

        if delay_in_seconds:
            target_date = datetime.utcnow() + timedelta(seconds=delay_in_seconds)
            timestamp = timestamp_pb2.Timestamp()
            timestamp.FromDatetime(target_date)

            task.schedule_time = timestamp

        try:
            response = self.client.create_task(parent=parent, task=task)
        except FailedPrecondition as e:
            if e.message != 'Queue does not exist.':
                raise

            self._create_queue(name=queue, location=location)
            response = self.client.create_task(parent=parent, task=task)
        return response

    def _create_queue(self, name, location=None):
        parent = f"projects/{self.project_id}/locations/{location or DEFAULT_LOCATION}"
        queue_name = self.client.queue_path(
            project=self.project_id,
            location=location or DEFAULT_LOCATION,
            queue=name,
        )

        queue = tasks_v2.Queue(
            name=queue_name,
        )
        return self.client.create_queue(
            parent=parent,
            queue=queue,
        )


class CloudSchedulerClient(GoogleCloudPilotAPI):
    _client_class = scheduler.CloudSchedulerClient
    DEFAULT_METHOD = scheduler.HttpMethod.POST

    def create(
            self,
            name,
            url,
            payload,
            cron,
            timezone=DEFAULT_TIMEZONE,
            method=DEFAULT_METHOD,
            headers=None,
            location=DEFAULT_LOCATION,
    ):
        parent = f"projects/{self.project_id}/locations/{location}"
        job = scheduler.Job(
            name=f'{parent}/jobs/{name}',
            schedule=cron,
            time_zone=timezone,
            http_target=scheduler.HttpTarget(
                uri=url,
                http_method=method,
                body=payload.encode(),
                headers=headers or {},
            )
        )

        response = self.client.create_job(
            request={
                "parent": parent,
                "job": job
            }
        )
        return response

    def update(
            self,
            name,
            url,
            payload,
            cron,
            timezone=DEFAULT_TIMEZONE,
            method=DEFAULT_METHOD,
            headers=None,
            location=DEFAULT_LOCATION,
    ):
        parent = f"projects/{self.project_id}/locations/{location}"
        job = scheduler.Job(
            name=f'{parent}/jobs/{name}',
            schedule=cron,
            time_zone=timezone,
            http_target=scheduler.HttpTarget(
                uri=url,
                http_method=method,
                body=payload.encode(),
                headers=headers or {},
            )
        )

        response = self.client.update_job(
            job=job,
        )
        return response

    def get(self, name, location=DEFAULT_LOCATION):
        response = self.client.get_job(
            name=f"projects/{self.project_id}/locations/{location}/jobs/{name}",
        )
        return response

    def delete(self, name, location=DEFAULT_LOCATION):
        response = self.client.delete_job(
            name=f"projects/{self.project_id}/locations/{location}/jobs/{name}",
        )
        return response

    def put(
            self,
            name,
            url,
            payload,
            cron,
            timezone=DEFAULT_TIMEZONE,
            method=DEFAULT_METHOD,
            headers=None,
            location=DEFAULT_LOCATION,
    ):
        try:
            response = self.update(
                name=name,
                url=url,
                payload=payload,
                cron=cron,
                timezone=timezone,
                method=method,
                headers=headers,
                location=location,
            )
        except NotFound:
            response = self.create(
                name=name,
                url=url,
                payload=payload,
                cron=cron,
                timezone=timezone,
                method=method,
                headers=headers,
                location=location,
            )
        return response
