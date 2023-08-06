import sys

from .spl_base_command import SplBaseCommand


class SplStreamingBatchCommand(SplBaseCommand):
    def process_data(self, parser, argv=None, input_stream=sys.stdin.buffer, output_stream=sys.stdout.buffer):
        while True:
            execute_meta = self.process_protocol_execute(input_stream, parser)
            resp = self.streaming_handle(self.lines)
            parser.send_packet(output_stream, execute_meta, resp)
            self.lines = []
            if self.is_finish:
                break
