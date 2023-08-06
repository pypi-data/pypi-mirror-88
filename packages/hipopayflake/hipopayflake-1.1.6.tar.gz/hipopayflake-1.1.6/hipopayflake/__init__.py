""" HipopayFlake - 64bit

    0 - 00000000 00000000 00000000 00000000 00000000 0 - 00 - 00000000 000 - 00000000 0
    1bit符号位(保留) - 41bit时间戳 - 2bit回拨调整位 - 11bit机器ID(5bit集群ID + 6bitWORKERID) - 9bit序列号


    1. 5bit集群ID最大支持 -1 ^ (-1 << 5) = 31个集群，目前来说就是31台服务器。

    2. 6bitWORKERID最大支持 -1 ^ (-1 << 6) = 63个worker,  目前一台机器共2 * cpu_count(4核CPU) + 1 = 9个worker，如果要达到顶点63个worker，则需要31核CPU。

    3. 9bit序列号最大支持 -1 ^ (-1 << 9) = 511个序列值，也就是说同一个集群中同一台机器在同一毫秒内可以生成511个递增ID。

"""

from datetime import datetime


__Author__ = 'KuangQingxu'


class HipopayIDWorker(object):

    _timestamp = -1
    _timestamp_start = 1600574880000
    _clock_backwards = 0
    _bits_clock_backwards = 2
    _bits_center_id = 5
    _bits_worker_id = 6
    _max_worker_id = -1 ^ (-1 << _bits_worker_id)
    _max_center_id = -1 ^ (-1 << _bits_center_id)
    _bits_sequence = 9

    _worker_id_shift = _bits_sequence
    _center_id_shift = (_worker_id_shift + _bits_worker_id)
    _clock_backwards_shift = (_center_id_shift + _bits_center_id)
    _timestamp_shift = (_clock_backwards_shift + _bits_clock_backwards)

    _sequence_mask = -1 ^ (-1 << _bits_sequence)
    _clock_backwards_mask = -1 ^ (-1 << _bits_clock_backwards)

    def __init__(self, center_id, worker_id, sequence):

        try:
            center_id = int(center_id)
            worker_id = int(worker_id)
            sequence = int(sequence)
        except Exception:
            raise ValueError('worker_id/center_id/sequence need `int`')

        if (center_id < 0) or (center_id > self._max_center_id):
            raise ValueError('center_id {0} error'.format(center_id))

        if (worker_id < 0) or (worker_id > self._max_worker_id):
            raise ValueError('worker_id {0} error'.format(worker_id))

        self._worker_id = worker_id
        self._center_id = center_id
        self._sequence = sequence

    def next_id(self):

        ts_now = self._generate_timestamp()

        if ts_now < self._timestamp:
            self._clock_backwards = (self._clock_backwards + 1) \
                & self._clock_backwards_mask

        if ts_now == self._timestamp:
            self._sequence = (self._sequence + 1) & self._sequence_mask
            if self._sequence == 0:
                ts_now = self._wait_next_timestamp(self._timestamp)
        else:
            self._sequence = 0

        self._timestamp = ts_now

        return ((ts_now - self._timestamp_start) << self._timestamp_shift) | \
            (self._clock_backwards << self._clock_backwards_shift) | \
            (self._center_id << self._center_id_shift) | \
            (self._worker_id << self._worker_id_shift) | \
            self._sequence

    def _generate_timestamp(self):
        return int(float(datetime.now().strftime('%s.%f')) * 1000)

    def _wait_next_timestamp(self, last_timestamp):
        ts_now = self._generate_timestamp()
        while(ts_now < last_timestamp):
            ts_now = self._generate_timestamp()
        return ts_now


if __name__ == '__main__':

    worker = HipopayIDWorker(1, 1, 1)

    for _ in range(0, 30000):
        x = worker.next_id()
        print('------> {0}'.format(x))
