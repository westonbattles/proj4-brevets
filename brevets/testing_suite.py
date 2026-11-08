import arrow
import acp_times


START = arrow.get(0).isoformat()

def test_open_general():
    # OPEN TIMES
    # 205 control for a 200 brevet must have open time 5H28M from start time
    assert acp_times.open_time(205, 200, START) == arrow.get(0).shift(hours=5,minutes=53).isoformat()
    # 550 control for a 600 brevet must have open time 17H8M from start time
    assert acp_times.open_time(550, 600, START) == arrow.get(0).shift(hours=17,minutes=8).isoformat()
    # 890 control for a 1000 brevet must have open time 29H9M from start time
    assert acp_times.open_time(890, 1000, START) == arrow.get(0).shift(hours=29,minutes=9).isoformat()
    # 1005 control for a 1000 brevet must have open time 33H5M from start time
    assert acp_times.open_time(1005, 1000, START) == arrow.get(0).shift(hours=33,minutes=5).isoformat()
    # 1200 control for a 1000 brevet must have open time 33H5M from start time
    assert acp_times.open_time(1200, 1000, START) == arrow.get(0).shift(hours=24+9, minutes=5).isoformat()

def test_close_general():
    # CLOSE TIMES
    assert acp_times.close_time(205, 200, START) == arrow.get(0).shift(hours=13,minutes=30).isoformat()
    assert acp_times.close_time(1000, 1000, START) == arrow.get(0).shift(hours=75).isoformat()
    assert acp_times.close_time(1000, 1000, START) == arrow.get(0).shift(hours=75).isoformat()
    assert acp_times.close_time(1200, 1000, START) == arrow.get(0).shift(hours=75).isoformat()
    assert acp_times.close_time(10, 1000, START) == arrow.get(0).shift(hours=1, minutes=30).isoformat()

def test_350km():
    assert acp_times.open_time(350, 600, START) == arrow.get(START).shift(hours=10, minutes=34).isoformat()


def test_550km():
    assert acp_times.open_time(550, 600, START) == arrow.get(START).shift(hours=17, minutes=8).isoformat()
    assert acp_times.close_time(550, 600, START) == arrow.get(START).shift(hours=36, minutes=40).isoformat()


def test_890km():
    assert acp_times.open_time(890, 1000, START) == arrow.get(START).shift(hours=29, minutes=9).isoformat()
    assert acp_times.close_time(890, 1000, START) == arrow.get(START).shift(hours=65, minutes=23).isoformat()


def test_1000km():
    assert acp_times.open_time(1200, 1000, START) == arrow.get(START).shift(hours=33, minutes=5).isoformat()
    assert acp_times.close_time(1200, 1000, START) == arrow.get(START).shift(hours=75).isoformat()


def test_400km():
    assert acp_times.close_time(400, 400, START) == arrow.get(START).shift(hours=27).isoformat()


def test_10km():
    assert acp_times.close_time(10, 200, START) == arrow.get(START).shift(hours=1, minutes=30).isoformat()