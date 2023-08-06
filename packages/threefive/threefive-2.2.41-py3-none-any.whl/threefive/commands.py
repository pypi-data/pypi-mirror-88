from base64 import b64encode
from .tools import i2b, reserve, to_stderr


class SpliceCommand:
    """
    Base class for all splice command classes,
    not used directly.
    """

    def __init__(self):
        self.break_auto_return = None
        self.break_duration = None
        self.time_specified_flag = None
        self.pts_time = None

    def decode(self, bitbin):
        return None

    def parse_break(self, bitbin):
        self.break_auto_return = bitbin.asflag(1)
        bitbin.forward(6)
        self.break_duration = bitbin.as90k(33)

    def encode_break(self):  # 40bits
        break_bytes = self.break_auto_return << 39
        break_bytes += reserve(6) << 33  # forward 6
        break_bytes += int(self.break_duration * 90000)
        return i2b(break_bytes, 5)

    def splice_time(self, bitbin):  # 40bits
        self.time_specified_flag = bitbin.asflag(1)
        if self.time_specified_flag:
            bitbin.forward(6)
            self.pts_time = bitbin.as90k(33)
        else:
            bitbin.forward(7)

    def encode_splice_time(self):
        if self.time_specified_flag:
            st_bytes = self.time_specified_flag << 39
            st_bytes += reserve(6) << 33  # forward six bits
            st_bytes += int(self.pts_time * 90000)
            return i2b(st_bytes, 5)

        else:

            return i2b(reserve(7), 1)


class SpliceNull(SpliceCommand):
    """
    Table 7 - splice_null()
    """

    def __init__(self):
        self.name = "Splice Null"
        self.splice_command_length = 0


class SpliceSchedule(SpliceCommand):
    """
    Table 8 - splice_schedule()
    """

    def __init__(self):
        self.name = "Splice Schedule"

    def decode(self, bitbin):
        splice_count = bitbin.asint(8)
        for i in range(0, splice_count):
            self.splice_event_id = bitbin.asint(32)
            self.splice_event_cancel_indicator = bitbin.asflag(1)
            bitbin.forward(7)
            if not self.splice_event_cancel_indicator:
                self.out_of_network_indicator = bitbin.asflag(1)
                self.program_splice_flag = bitbin.asflag(1)
                self.duration_flag = bitbin.asflag(1)
                bitbin.forward(5)
                if self.program_splice_flag:
                    self.utc_splice_time = bitbin.asint(32)
                else:
                    self.component_count = bitbin.asint(8)
                    self.components = []
                    for j in range(0, self.component_count):
                        self.components[j] = {
                            "component_tag": bitbin.asint(8),
                            "utc_splice_time": bitbin.asint(32),
                        }
                if self.duration_flag:
                    self.break_duration(bitbin)
                self.unique_program_id = bitbin.asint(16)
                self.avail_num = bitbin.asint(8)
                self.avails_expected = bitbin.asint(8)


class SpliceInsert(SpliceCommand):
    """
    Table 9 - splice_insert()
    """

    def __init__(self):
        super().__init__()
        self.name = "Splice Insert"
        self.splice_event_id = None
        self.splice_event_cancel_indicator = None
        self.out_of_network_indicator = None
        self.program_splice_flag = None
        self.duration_flag = None
        self.splice_immediate_flag = None
        self.component_count = None
        self.unique_program_id = None
        self.avail_num = None
        self.avail_expected = None

    def decode(self, bitbin):
        self.splice_event_id = bitbin.asint(32)  # uint32
        self.splice_event_cancel_indicator = bitbin.asflag(1)
        bitbin.forward(7)  # uint8
        if not self.splice_event_cancel_indicator:
            self.out_of_network_indicator = bitbin.asflag(1)
            self.program_splice_flag = bitbin.asflag(1)
            self.duration_flag = bitbin.asflag(1)
            self.splice_immediate_flag = bitbin.asflag(1)
            bitbin.forward(4)  # uint8
            if self.program_splice_flag and not self.splice_immediate_flag:
                self.splice_time(bitbin)  # uint8 + uint32
            if not self.program_splice_flag:
                self.component_count = bitbin.asint(8)  # uint 8
                self.components = []
                for i in range(0, self.component_count):
                    self.components[i] = bitbin.asint(8)
                if not self.splice_immediate_flag:
                    self.splice_time(bitbin)
            if self.duration_flag:
                self.parse_break(bitbin)
            self.unique_program_id = bitbin.asint(16)
            self.avail_num = bitbin.asint(8)
            self.avail_expected = bitbin.asint(8)

    def encode(self):
        bencoded = i2b(self.splice_event_id, 4)
        bencoded += i2b((self.splice_event_cancel_indicator << 7) + reserve(7), 1)
        if not self.splice_event_cancel_indicator:
            four_flags = self.out_of_network_indicator << 7
            four_flags += self.program_splice_flag << 6
            four_flags += self.duration_flag << 5
            four_flags += self.splice_immediate_flag << 4
            four_flags += reserve(4)
            bencoded += i2b(four_flags, 1)
            if self.program_splice_flag and not self.splice_immediate_flag:
                bencoded += self.encode_splice_time()
            if not self.program_splice_flag:
                bencoded += i2b(self.component_count, 1)
                for i in range(0, self.component_count):
                    bencoded += i2b(self.components[i], 1)
                if not self.splice_immediate_flag:
                    bencoded += self.encode_splice_time()
            if self.duration_flag:
                bencoded += self.encode_break()
            bencoded += i2b(self.unique_program_id, 2)
            bencoded += i2b(self.avail_num, 1)
            bencoded += i2b(self.avail_expected, 1)
            to_stderr(bencoded)


class TimeSignal(SpliceCommand):
    """
    Table 10 - time_signal()
    """

    def __init__(self):
        super().__init__()
        self.name = "Time Signal"

    def decode(self, bitbin):
        self.splice_time(bitbin)

    def encode(self):
        command_bytes = self.encode_splice_time()
        return command_bytes


class BandwidthReservation(SpliceCommand):
    """
    Table 11 - bandwidth_reservation()
    """

    def __init__(self):
        self.name = "Bandwidth Reservation"


class PrivateCommand(SpliceCommand):
    """
    Table 12 - private_command()
    """

    def __init__(self):
        self.name = "Private Command"
        self.identifier = None

    def decode(self, bitbin):
        self.identifier = bitbin.asint(32)

    def encode(self):
        command_bytes = i2b(self.identifier, 4)
        return command_bytes
