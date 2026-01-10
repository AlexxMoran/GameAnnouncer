from enums.registration_status import RegistrationStatus
from enums import RegistrationStatus as RegistrationStatusFromPackage


def test_registration_status_values():
    assert RegistrationStatus.PENDING.value == "pending"
    assert RegistrationStatus.APPROVED.value == "approved"
    assert RegistrationStatus.REJECTED.value == "rejected"
    assert RegistrationStatus.CANCELLED.value == "cancelled"


def test_registration_status_from_value():
    assert RegistrationStatus("pending") is RegistrationStatus.PENDING
    assert RegistrationStatus("approved") is RegistrationStatus.APPROVED


def test_registration_status_iterable_and_names():
    names = {s.name for s in RegistrationStatus}
    assert names == {"PENDING", "APPROVED", "REJECTED", "CANCELLED", "EXPIRED"}

    values = {s.value for s in RegistrationStatus}
    assert values == {"pending", "approved", "rejected", "cancelled", "expired"}


def test_import_from_package():
    assert RegistrationStatusFromPackage is RegistrationStatus
