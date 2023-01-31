from dataclasses import dataclass


@dataclass
class MethodNode:
    start_line: int
    stop_line: int
    source_code: str

    def __str__(self):
        return f"MethodNode(lines {self.start_line} to {self.stop_line})"
