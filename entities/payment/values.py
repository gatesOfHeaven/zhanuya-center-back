from enum import Enum


class PaymentMethod(Enum):
    CACHE = 'cache'
    CARD = 'Bank Card'
    KASPI_QR = 'Kaspi QR'
    HALYK_QR = 'Halyk QR'
    JUSAN_QR = 'Jusan QR'


class ProviderType(Enum):
    TERMINAL = 'terminal'
    MANAGER = 'manager'