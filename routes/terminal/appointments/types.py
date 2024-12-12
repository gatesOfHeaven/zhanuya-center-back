from pydantic import BaseModel, Field

from core.bases import BaseResponse
from core.facades import calc
from entities.user import UserAsForeign
from entities.doctor import DoctorAsForeign
from entities.category import CategoryAsForeign
from entities.room import RoomAsPrimary
from entities.appointment_type import AppointmentTypeAsForeign
from entities.slot import Slot
from entities.payment import PaymentMethod


class ConfirmAppointmentReq(BaseModel):
    method: PaymentMethod = Field(PaymentMethod.CASH)
    confirmationCode: int = Field(lt = 10 ** 4)


class AppointmentAsElement(BaseResponse):
    id: int
    startTime: str
    endTime: str
    office: str
    patient: UserAsForeign
    doctor: UserAsForeign

    @staticmethod
    def to_json(appointment: Slot):
        doctor = appointment.workday.doctor
        return AppointmentAsElement(
            id = appointment.id,
            startTime = calc.time_to_str(appointment.starts_at, '%H:%M:%S'),
            endTime = calc.time_to_str(appointment.ends_at, '%H:%M:%S'),
            office = appointment.workday.doctor.office.title,
            type = AppointmentTypeAsForeign.to_json(appointment.type),
            patient = UserAsForeign.to_json(appointment.patient),
            doctor = UserAsForeign.to_json(doctor.profile)
        ).model_dump()


class SlotAsPrimary(BaseResponse):
    id: int
    date: str
    index: int
    startTime: str
    endTime: str
    price: int
    office: str
    type: AppointmentTypeAsForeign
    category: CategoryAsForeign
    doctor: DoctorAsForeign
    patient: UserAsForeign

    @staticmethod
    def to_json(appointment: Slot):
        return SlotAsPrimary(
            id = appointment.id,
            date = calc.time_to_str(appointment.workday.date),
            index = appointment.index,
            startTime = calc.time_to_str(appointment.starts_at, '%H:%M:%S'),
            endTime = calc.time_to_str(appointment.ends_at, '%H:%M:%S'),
            price = appointment.price,
            office = appointment.workday.doctor.office.title,
            type = AppointmentTypeAsForeign.to_json(appointment.type),
            category = CategoryAsForeign.to_json(appointment.workday.doctor.category),
            doctor = DoctorAsForeign.to_json(appointment.workday.doctor),
            patient = UserAsForeign.to_json(appointment.patient)
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