from pydantic import BaseModel, Field

from core.bases import BaseResponse
from core.facades import calc
from entities.user import UserAsForeign
from entities.category import CategoryAsForeign
from entities.appointment_type import AppointmentTypeAsForeign
from entities.slot import Slot
from entities.payment import PaymentMethod


class ConfirmAppointmentReq(BaseModel):
    method: PaymentMethod = Field(PaymentMethod.CACHE)
    confirmationCode: int = Field(lt = 10 ** 4)


class AppointmentAsElement(BaseResponse):
    id: int
    startTime: str
    endTime: str
    type: AppointmentTypeAsForeign
    patient: UserAsForeign
    doctor: UserAsForeign
    category: CategoryAsForeign

    @staticmethod
    def to_json(appointment: Slot):
        doctor = appointment.workday.doctor
        return AppointmentAsElement(
            id = appointment.id,
            startTime = calc.time_to_str(appointment.starts_at, '%H:%M:%S'),
            endTime = calc.time_to_str(appointment.ends_at, '%H:%M:%S'),
            type = AppointmentTypeAsForeign.to_json(appointment.type),
            patient = UserAsForeign.to_json(appointment.patient),
            doctor = UserAsForeign.to_json(doctor.profile),
            category = CategoryAsForeign.to_json(doctor.category)
        ).model_dump()


class AppointmentsToManage(BaseResponse):
    add: list[AppointmentAsElement]
    delete: list[int]

    @staticmethod
    def to_json(appointments_to_add: list[AppointmentAsElement], appointments_to_delete: list[int]):
        return AppointmentsToManage(
            add = appointments_to_add,
            delete = appointments_to_delete
        ).model_dump()