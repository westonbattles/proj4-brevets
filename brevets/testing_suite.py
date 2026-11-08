import arrow
import acp_times

def test_controls():
    # OPEN TIMES
    # 205 control for a 200 brevet must have open time 5H28M from start time
    assert acp_times.open_time(205, 200, arrow.get(0).isoformat()) == arrow.get(0).shift(hours=5,minutes=53).isoformat()
    # 550 control for a 600 brevet must have open time 17H8M from start time
    assert acp_times.open_time(550, 600, arrow.get(0).isoformat()) == arrow.get(0).shift(hours=17,minutes=8).isoformat()
    # 890 control for a 1000 brevet must have open time 29H9M from start time
    assert acp_times.open_time(890, 1000, arrow.get(0).isoformat()) == arrow.get(0).shift(hours=29,minutes=9).isoformat()
    # 1005 control for a 1000 brevet must have open time 33H5M from start time
    assert acp_times.open_time(1005, 1000, arrow.get(0).isoformat()) == arrow.get(0).shift(hours=33,minutes=5).isoformat()
    # 1200 control for a 1000 brevet must have open time 33H5M from start time
    assert acp_times.open_time(1200, 1000, arrow.get(0).isoformat()) == arrow.get(0).shift(hours=24+9, minutes=5).isoformat()

    # CLOSE TIMES
    assert acp_times.close_time(1000, 1000, arrow.get(0).isoformat()) == arrow.get(0).shift(hours=75).isoformat()
    assert acp_times.close_time(1200, 1000, arrow.get(0).isoformat()) == arrow.get(0).shift(hours=75).isoformat()
