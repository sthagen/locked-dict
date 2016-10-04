
import logging
import pickle
import random
import sys
import threading
import time

import pytest

import locked_dict


@pytest.mark.skip(reason='To be migrated from old school to pytest')
def test_locked_dict():
    """Simple test driver. Switch to debug logging, if any argument given."""

    _start = time.time()

    a_level = logging.INFO if len(sys.argv) < 2 else logging.DEBUG
    a_format = '%(asctime)s: %(message)s'

    logging.basicConfig(format=a_format)
    logger = logging.getLogger(__name__)
    logger.setLevel(a_level)

    def worker(key_seq, shared_map):
        for key in key_seq:
            shared_map[key] = {threading.currentThread().getName(): key}
            logger.debug('{} {}'.format(key, shared_map[key]))
            pause = float(random.randint(1, 5)) / 1000.
            logger.debug('sleeping %02.3f' % (pause,))
            time.sleep(pause)

        return len(key_seq)

    expected = 0
    d = locked_dict.LockedDict()
    with d as m:
        m[0] = ['foo']
        expected += 1
        m.clear()
        expected -= 1
        assert len(m) == expected
        try:
            # noinspection PyUnusedLocal
            __ = m.popitem()
            assert False
        except KeyError:
            pass
        try:
            del m['not_there']
            assert False
        except KeyError:
            pass
        m.update({0: 'foo'})
        expected += 1
        assert len(m) == expected

    logger.debug('Entries({:5d}/{:5d})'.format(len(d), expected))

    for k, v in d.items():
        logger.debug("{}: {}".format(k, v))
    logger.debug('{} {} {}'.format(
        id(d), isinstance(d, dict), isinstance(d, locked_dict.LockedDict)))
    logger.debug(dir(d))
    logger.debug(dir(getattr(d, '_lock')))

    with d as m:
        d_ser = pickle.dumps(m)
    logger.debug(d_ser)

    with d as m:
        m[1] = ('bar',)
        expected += 1
        m[42] = {'baz': 'ooka'}
        expected += 1
        x = m.pop(42)
        expected -= 1
        m[42] = x
        expected += 1
        __ = m.get(-42)
        assert __ is None
        if -42 not in m:
            __ = locked_dict.LockedDict.fromkeys(m.keys(), 'yes')
            bf = dict([(z, 'yes') for z in m.keys()])
            assert __ == bf
            assert __ is not bf
            logger.debug(__)

    with d as m:
        d_ser = pickle.dumps(m)
    logger.debug(d_ser)

    rd = pickle.loads(d_ser)
    for k, v in rd.items():
        logger.debug("{}: {}".format(k, v))

    logger.debug('Entries({:5d}/{:5d})'.format(len(rd), expected))

    logger.debug('{} {} {}'.format(
        id(rd), type(rd), isinstance(rd, (dict, locked_dict.LockedDict))))

    worker_tasks = random.randint(1, 234)
    worker_count = random.randint(5, 67)
    logger.debug("Starting {} workers on {} tasks each ..."
                 "".format(worker_count, worker_tasks))
    expected += worker_count * worker_tasks
    for i in range(43, 43 + worker_count * worker_tasks, worker_tasks):
        t = threading.Thread(
            target=worker, args=(range(i, i + worker_tasks), rd))
        t.setDaemon(True)
        t.start()

    main_thread = threading.currentThread()
    for t in threading.enumerate():
        if t is main_thread:
            continue
        logger.debug('joining %s' % (t.getName(),))
        t.join()

    for k, v in rd.items():
        logger.debug("{}: {}".format(k, v))
    assert len(rd) == expected
    logger.info(
        'WorkersTasks({:2d}:{:3d}).Entries({:5d}/{:5d}); SizeBytes({:6d})'
        ' - with Python({}); LatencySecs({:0.3f})'
        ''.format(worker_count, worker_tasks, len(rd), expected,
                  sys.getsizeof(rd),
                  ','.join(["{:2d}".format(z) for z in sys.version_info[:3]]),
                  round(time.time() - _start, 3)))


def test_main():
    assert locked_dict  # use your library here


@pytest.mark.skip(reason='Needs fixing of env and folders')
def test_stage():
    expected = 0
    d = locked_dict.LockedDict()
    assert len(d) == expected
    assert bool(d) is False
    assert d is not True
    assert hasattr(d, '_lock')

    empty_d = {}
    assert d == empty_d

    plain_old_d = {999: 'plain old dict', 12345: 54321}
    assert d != plain_old_d

    with d as m:
        assert len(m) == expected
        assert bool(m) is False
        assert m is not True
        assert hasattr(m, '_lock')
        assert m != plain_old_d
        assert m == empty_d

        m[0] = ['foo']
        expected += 1
        assert len(m) == expected
        assert bool(m) is True
        assert m is not False
        assert m != plain_old_d
        assert m != empty_d

        m.clear()
        expected -= 1
        assert len(m) == expected
        assert bool(m) is False
        assert m is not True
        assert m != plain_old_d
        assert m == empty_d

        with pytest.raises(KeyError):
            # noinspection PyUnusedLocal
            __ = m.popitem()

        with pytest.raises(KeyError):
            del m['not_there']

        m.update({0: 'foo'})
        expected += 1
        assert len(m) == expected
        assert bool(m) is True
        assert m is not False
        assert m != plain_old_d
        assert m != empty_d
