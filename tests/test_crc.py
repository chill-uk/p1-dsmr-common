from p1_dsmr_common.crc import calculate_crc, validate_crc


def test_validates_exact_raw_crc() -> None:
    body = "/TEST\r\n1-3:0.2.8(50)\r\n!"
    checksum = f"{calculate_crc(body.encode('ascii')):04X}"
    result = validate_crc(body + checksum + "\r\n")

    assert result.valid
    assert result.reported == checksum
    assert result.calculated == checksum


def test_rejects_missing_crc() -> None:
    result = validate_crc("/TEST\r\n!\r\n")

    assert not result.valid
    assert result.error == "missing or malformed CRC"
