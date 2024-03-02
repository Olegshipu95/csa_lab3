from __future__ import annotations
import struct
import json
from enum import Enum


class OpcodeParamType(str, Enum):
    CONST = "const"
    ADDR = "addr"
    UNDEFINED = "undefined"
    ADDR_REL = "addr_rel"


class OpcodeParam:
    def __init__(self, param_type: OpcodeParamType, value: any):
        self.param_type = param_type
        self.value = value

    def __str__(self):
        return f"({self.param_type}, {self.value})"


class OpcodeType(str, Enum):
    DROP = "drop"
    MUL = "mul"
    DIV = "div"
    SUB = "sub"
    ADD = "add"
    MOD = "mod"
    SWAP = "swap"
    OVER = "over"
    DUP = "dup"
    EQ = "eq"
    GR = "gr"
    LS = "ls"
    DI = "di"
    EI = "ei"
    OMIT = "omit"
    READ = "read"

    # not used in source code, compile-generated
    STORE = "store"
    LOAD = "load"
    PUSH = "push"
    RPOP = "rpop"  # move from return stack to data stack
    POP = "pop"  # move from data stack to return stack
    JMP = "jmp"
    ZJMP = "zjmp"
    CALL = "call"
    RET = "ret"
    HALT = "halt"

    def __str__(self):
        return str(self.value)


def get_number_of_OpcodeType(opcode: OpcodeType) -> int:
    return list(OpcodeType).index(opcode)


def get_opcode_by_number(number: int) -> OpcodeType:
    return list(OpcodeType)[number]


class Opcode:
    def __init__(self, opcode_type: OpcodeType, params: list[OpcodeParam]):
        self.opcode_type = opcode_type
        self.params = params


class TermType(Enum):
    (
        # Term --> Opcode
        DI,
        EI,
        DUP,
        ADD,
        SUB,
        MUL,
        DIV,
        MOD,
        OMIT,
        SWAP,
        DROP,
        OVER,
        EQ,
        LS,
        GR,
        READ,
        # Term !-> Opcode
        VARIABLE,
        ALLOT,
        STORE,
        LOAD,
        IF,
        ELSE,
        THEN,
        PRINT,
        DEF,
        RET,
        DEF_INTR,
        DO,
        LOOP,
        BEGIN,
        UNTIL,
        LOOP_CNT,
        CALL,
        STRING,
        ENTRYPOINT,
    ) = range(35)


def read_binary_code(filename: str):
    with open(filename, "rb") as file:
        binary_data = file.read()

    decoded_values = []

    # Расшифровка бинарных данных
    for i in range(0, len(binary_data), 4):  # Предполагается, что каждое значение кодируется 4 байтами
        struct_bytes = binary_data[i : i + 4]
        decoded_value = struct.unpack("<I", struct_bytes)[0]

        # Извлечение значений из битовых полей
        opcode_number = decoded_value >> 27
        index = (decoded_value >> 12) & 0x7FFF  # Маска для извлечения 15 бит адреса
        arg = decoded_value & 0xFFF  # Маска для извлечения 12 бит аргумента
        tuple_decode = {"index": index, "command": get_opcode_by_number(opcode_number).value, "arg": arg}
        # print(tuple_decode)
        decoded_values.append(tuple_decode)
    return decoded_values


def write_code(filename: str, code: bytes):
    with open(filename, "wb") as file:
        file.write(code)


def read_code(source_path: str) -> list:
    with open(source_path, encoding="utf-8") as file:
        return json.loads(file.read())
