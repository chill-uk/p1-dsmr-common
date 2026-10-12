from p1_dsmr_common.redaction import redact_equipment_ids


def test_redacts_equipment_ids() -> None:
    telegram = (
        "0-0:96.1.1(ABCDEF)\r\n"
        "0-1:96.1.0(123456)\r\n"
        "1-0:1.7.0(00.123*kW)\r\n"
    )

    redacted = redact_equipment_ids(telegram)

    assert "ABCDEF" not in redacted
    assert "123456" not in redacted
    assert "1-0:1.7.0(00.123*kW)" in redacted
