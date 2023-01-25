class MethodNode:
    start = None
    stop = None

    def get_start_line(self):
        return self.start.line

    def get_stop_line(self):
        return self.stop.line

    def get_source_code(self):
        return self.start.source[1].strdata[self.start.start:self.stop.stop]

    def __str__(self):
        return f"MethodNode(lines {self.get_start_line()} to {self.get_stop_line()})"
