from typing import List

from django_cloud_tasks.management.commands import BaseInitCommand


class Command(BaseInitCommand):
    action = 'schedule'
    name = 'tasks'

    async def perform_init(self, app_config) -> List[str]:
        return await app_config.schedule_tasks()
