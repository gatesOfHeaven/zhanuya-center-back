from pydantic import BaseModel, Field

from entities.payment import PaymentMethod


class ConfirmAppointmentReq(BaseModel):
    method: PaymentMethod = Field(PaymentMethod.CACHE)
    confirmationCode: int = Field(lt = 10 ** 4)