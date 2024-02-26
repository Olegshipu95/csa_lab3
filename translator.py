from isa import write_code
import sys


class Term:
    def __init__(self, word_number: int, term_type: TermType | None, word: str):
        self.converted = False
        self.operand = None
        self.word_number = word_number
        self.term_type = term_type
        self.word = word

def translate(source_code: str) -> list[dict]:
    pass


def main(source_file: str, target_file: str) -> None:
    with open(source_file, encoding="utf-8") as f:
        source_code = f.read()
    code = translate(source_code)
    write_code(target_file, code)
    print("source LoC:", len(source_code.split("\n")), "code instr:", len(code))


if __name__ == "__main__":
    assert len(sys.argv) == 3, "Wrong arguments: translator.py <input_file> <target_file>"
    _, source, target = sys.argv
    main(source, target)
