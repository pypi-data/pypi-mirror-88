from typing import Optional
import pytest
from psec import mac


@pytest.mark.parametrize(
    ["data", "block_len", "result"],
    [
        ("1234", 8, "1234000000000000"),
        ("1234567890123456", 8, "1234567890123456"),
        ("1234", None, "1234000000000000"),
        ("1234567890123456", None, "1234567890123456"),
        ("1234", 4, "12340000"),
        ("12345678", 4, "12345678"),
        ("", 4, "00000000"),
    ],
)
def test_pad_iso9797_1(data: str, block_len: Optional[int], result: str) -> None:
    assert result == mac.pad_iso9797_1(bytes.fromhex(data), block_len).hex()


@pytest.mark.parametrize(
    ["data", "block_len", "result"],
    [
        ("1234", 8, "1234800000000000"),
        ("12345678901234", 8, "1234567890123480"),
        ("1234567890123456", 8, "12345678901234568000000000000000"),
        ("1234", None, "1234800000000000"),
        ("12345678901234", None, "1234567890123480"),
        ("1234567890123456", None, "12345678901234568000000000000000"),
        ("1234", 4, "12348000"),
        ("123456", 4, "12345680"),
        ("12345678", 4, "1234567880000000"),
        ("", 4, "80000000"),
    ],
)
def test_pad_iso9797_2(data: str, block_len: Optional[int], result: str) -> None:
    assert result == mac.pad_iso9797_2(bytes.fromhex(data), block_len).hex()


@pytest.mark.parametrize(
    ["data", "block_len", "result"],
    [
        ("1234", 8, "00000000000000101234000000000000"),
        ("1234567890123456", 8, "00000000000000401234567890123456"),
        ("1234", None, "00000000000000101234000000000000"),
        ("1234567890123456", None, "00000000000000401234567890123456"),
        ("1234", 4, "0000001012340000"),
        ("12345678", 4, "0000002012345678"),
        ("", 4, "0000000000000000"),
    ],
)
def test_pad_iso9797_3(data: str, block_len: Optional[int], result: str) -> None:
    assert result == mac.pad_iso9797_3(bytes.fromhex(data), block_len).hex()


def test_mac_iso9797_3_exception() -> None:
    with pytest.raises(
        ValueError,
        match="Specify valid padding method: 1, 2 or 3.",
    ):
        mac.mac_iso9797_3(
            b"AAAAAAAAAAAAAAAA",
            b"BBBBBBBBBBBBBBBB",
            b"hello world",
            4,
        )


@pytest.mark.parametrize(
    ["padding", "length", "result"],
    [
        (1, 8, "3DDE5C5511661CBF"),
        (2, 8, "E16941032C3BC7D4"),
        (3, 8, "BA90F750EF43F668"),
        (1, None, "3DDE5C5511661CBF"),
        (2, None, "E16941032C3BC7D4"),
        (3, None, "BA90F750EF43F668"),
        (1, 4, "3DDE5C55"),
        (2, 4, "E1694103"),
        (3, 4, "BA90F750"),
    ],
)
def test_mac_iso9797_3(padding: int, length: Optional[int], result: str) -> None:
    assert result == (
        mac.mac_iso9797_3(
            b"AAAAAAAAAAAAAAAA", b"BBBBBBBBBBBBBBBB", b"hello world", padding, length
        )
        .hex()
        .upper()
    )
