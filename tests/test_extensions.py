from dsmr_parser import telegram_specifications
from dsmr_parser.parsers import TelegramParser

from p1_dsmr_common.extensions import extended_spec


def test_total_counters_are_available_through_extended_spec() -> None:
    parser = TelegramParser(
        extended_spec(telegram_specifications.V5),
        apply_checksum_validation=False,
    )
    telegram = (
        "/XYZ5\\TEST\r\n"
        "1-3:0.2.8(50)\r\n"
        "1-0:1.8.0(010000.123*kWh)\r\n"
        "1-0:2.8.0(000500.456*kWh)\r\n"
        "!ABCD\r\n"
    )

    parsed = parser.parse(telegram)

    assert float(parsed.ELECTRICITY_IMPORTED_TOTAL.value) == 10000.123
    assert float(parsed.ELECTRICITY_EXPORTED_TOTAL.value) == 500.456
