import json
import sys

class SplPacketUtils(object):
    def parse_head(self, input_stream=sys.stdin.buffer):
        try:
            header = input_stream.readline().decode("utf-8")
        except Exception as error:
            raise RuntimeError('Failed to read spl protocol header: {}'.format(error))
        parts = str.split(header, ",")
        meta_length = int(parts[1])
        body_length = int(parts[2])

        return meta_length, body_length

    def parse_meta(self, input_stream=sys.stdin.buffer, length=0):
        try:
            meta_body = input_stream.read(length).decode("utf-8")
            metainfo = json.loads(meta_body)
        except Exception as error:
            raise RuntimeError('Failed to parser spl protocol meta: {}'.format(error))

        return metainfo

    def parse_body(self, input_stream=sys.stdin.buffer, length=0):
        records = []
        if length <= 0:
            return records

        try:
            body = input_stream.read(length).decode("utf-8")
            rows = str.split(body, '\n')
            if len(rows) < 2:
                return records

            fields = str.split(rows[0], '\t')
            for row in rows[1:]:
                record = {}
                parts = str.split(row, '\t')
                for i in range(len(fields)):
                    if i < len(parts):
                        record[fields[i]] = self.format_field(parts[i])
                records.append(record)

            return records
        except Exception as error:
            raise RuntimeError('Failed to parser spl protocol body: {}'.format(error))

    def format_field(self, part):
        type, value = str.split(part, ',', 1)
        if int(type) == 0:
            return self.decode_string(value)
        elif int(type) == 1:
            return int(value)
        elif int(type) == 2:
            return float(value)
        elif int(type) == 3:
            return ''
        elif int(type) == 4:
            return str.islower(value) == 'true'
        elif int(type) == 5:
            return value
        return value


    def send_packet(self, output_stream=sys.stdout.buffer, meta_info=None, lines=None):
        if meta_info is None:
            meta_info = {}
        if lines is None:
            lines = []
        meta = json.dumps(meta_info).encode("utf-8")

        body = self.convert_body_to_str(lines).encode("utf-8")

        head = ('chunked 1.0,%s,%s\n' % (len(meta), len(body))).encode("utf-8")
        output_stream.write(head)
        output_stream.write(meta)
        if len(body) > 0:
            output_stream.write(body)

        output_stream.flush()
        return

    def convert_body_to_str(self, lines=[]):
        if lines is None:
            return ''

        if len(lines) == 0:
            return ''

        field_str = ""
        line_strs = []
        fields = []
        allfields = {}
        for line in lines:
            if not isinstance(line, dict):
                continue
            row = dict(line)
            line_str = ''
            if len(fields) != 0:
                for field in fields:
                    if field not in row:
                        line_str += '\t'
                    else:
                        line_str = line_str + self.encode_string(str(row[field])) + '\t'

            for key in row:
                if key in allfields:
                    continue
                allfields[key] = 0
                fields.append(key)
                line_str = line_str + self.encode_string(str(row[key])) + '\t'

            line_strs.append(line_str[:len(line_str) - 1])

        for field in fields:
            field_str = field_str + field + '\t'

        field_str = field_str[:len(field_str) - 1]

        body = field_str
        for line_str in line_strs:
            body += '\n' + line_str

        return body

    def encode_string(self, value):
        value = str.replace(value, '\t', '\\t')
        value = str.replace(value, '\n', '\\n')
        return value

    def decode_string(self, value):
        value = str.replace(value, '\\t', '\t')
        value = str.replace(value, '\\n', '\n')
        return value
