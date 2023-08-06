from enum import Flag


def has_flag(value: Flag, accepted: Flag) -> bool:
    return value & accepted == accepted
