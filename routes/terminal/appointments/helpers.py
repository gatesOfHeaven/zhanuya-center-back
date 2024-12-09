from entities.slot import Slot


def key_for(appointment: Slot) -> str:
    return f'appointment:{appointment.id}'