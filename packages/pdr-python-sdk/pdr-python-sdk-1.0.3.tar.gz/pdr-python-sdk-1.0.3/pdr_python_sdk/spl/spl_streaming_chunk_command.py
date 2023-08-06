import sys

from .spl_base_command import SplBaseCommand


class SplStreamingChunkCommand(SplBaseCommand):

    def process_data(self, parser, argv=None, input_stream=sys.stdin.buffer, output_stream=sys.stdout.buffer):
        if argv is None:
            argv = sys.argv
        while True:
            execute_meta = self.process_protocol_execute(input_stream, parser)
            if self.is_finish:
                resp = self.streaming_handle(self.lines)
                parser.send_packet(output_stream, execute_meta, resp)
                break
            parser.send_packet(output_stream, execute_meta, '')
