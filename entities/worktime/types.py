from utils.bases import BaseResponse
from .entity import Worktime


class WorktimeAsForeign(BaseResponse):
    startHours: int
    endHours: int

    @staticmethod
    def to_json(worktime: Worktime):
        return WorktimeAsForeign(
            startHours = worktime.starts_at,
            endHours = worktime.ends_at
        ).model_dump()