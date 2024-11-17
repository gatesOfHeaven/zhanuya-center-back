from pytest import mark
from httpx import AsyncClient
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta

from utils.facades import week, calc
from entities.user.factory import Factory as UserFactory
from entities.doctor.factory import Factory as DoctorFactory
from routes.patient.doctors import FreeSlotsRes
from routes.patient.appointments import SlotAsPrimary, PatientAsForeign, MakeAppointmentReq, MySlotAsElement
from tests.utils.app import anyio_backend, client
from tests.utils.db import temp_db


@mark.anyio
@mark.parametrize(
    ('appointment_type_id', 'slot_duration'),
    [ (1, 30), (2, 30), (2, 60) ]
)
async def test_appointments_crud(
    appointment_type_id: int,
    slot_duration: int,
    client: AsyncClient,
    temp_db: AsyncSession,
    anyio_backend
):
    route = '/patient/appointments'
    user_query = UserFactory(temp_db)
    patient, token = await user_query.new()
    headers = { 'Auth': f'Bearer {token}' }
    
    for doctor in await DoctorFactory(temp_db).get_random(10):
        for day in week.get_week(week_num = 1):
            date_str = calc.time_to_str(day)
            # free slots
            response = await client.get(
                url = f'/patient/doctors/{doctor.id}/day/{date_str}',
                params = { 'duration': slot_duration }
            )
            assert response.status_code == status.HTTP_200_OK

            free_slots = FreeSlotsRes(**response.json()).freeSlots
            total_free_time = timedelta(microseconds = 0)
            for slot in free_slots:
                total_free_time += slot.duration()
            if total_free_time < timedelta(hours = 2):
                continue

            appointment_id = 0
            for empty_slot in free_slots:
                if appointment_id == 0:
                    # make appointment
                    response = await client.post(
                        url = route,
                        headers = headers,
                        json = MakeAppointmentReq(
                            doctorId = doctor.id,
                            date = date_str,
                            typeId = appointment_type_id,
                            startsAt = empty_slot.startTime,
                            endsAt = empty_slot.endTime
                        ).model_dump()
                    )
                    assert response.status_code == status.HTTP_201_CREATED
                else:
                    # update appointment
                    response = await client.put(
                        url = f'{route}/{appointment_id}',
                        headers = headers,
                        json = MakeAppointmentReq(
                            doctorId = doctor.id,
                            date = date_str,
                            typeId = appointment_type_id,
                            startsAt = empty_slot.startTime,
                            endsAt = empty_slot.endTime
                        ).model_dump()
                    )
                    assert response.status_code == status.HTTP_200_OK

                # my appointments
                response = await client.get(route, headers = headers)
                my_appointments = [
                    MySlotAsElement(**appointment)
                    for appointment in response.json()
                ]
                appointment_id = my_appointments[0].id
                assert response.status_code == status.HTTP_200_OK
                assert len(my_appointments) == 1

                # read appointment
                response = await client.get(f'{route}/{appointment_id}', headers = headers)
                my_appointment = SlotAsPrimary(**response.json())
                assert response.status_code == status.HTTP_200_OK
                assert my_appointment.id == appointment_id
                assert my_appointment.startTime == empty_slot.startTime
                assert my_appointment.endTime == empty_slot.endTime
                assert my_appointment.patient.model_dump() == PatientAsForeign.to_json(patient)
            
            # delete appointment
            response = await client.delete(f'{route}/{appointment_id}', headers = headers)
            assert response.status_code == status.HTTP_200_OK
            response = await client.get(f'{route}/{appointment_id}', headers = headers)
            assert response.status_code == status.HTTP_404_NOT_FOUND
            response = await client.get(route, headers = headers)
            my_appointments = [
                MySlotAsElement(**appointment)
                for appointment in response.json()
            ]
            assert response.status_code == status.HTTP_200_OK
            assert my_appointments == []

    await user_query.remove(patient)