"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_alg.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow



#  Note for CIS 322 Fall 2016:
#  You MUST provide the following two functions
#  with these signatures, so that I can write
#  automated tests for grading.  You must keep
#  these signatures even if you don't use all the
#  same arguments.  Arguments are explained in the
#  javadoc comments.
#


# control location (exclusive): min speed (km/h), max speed (km/h)
ACP_MIN_MAX_TABLE = {
    200: [15, 34],
    400: [15, 32],
    600: [15, 30],
    1000: [11.428, 28],
    1300: [13.333, 26]
}

def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
       brevet_dist_km: number, the nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """

    return calculate_time(control_dist_km, brevet_dist_km, brevet_start_time, 1)
    


def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
          brevet_dist_km: number, the nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """

    start = arrow.get(brevet_start_time)

    # french variation (controls from 0-60 are based on 20km/h (3km/min))
    if 0 <= control_dist_km < 60:
        minutes = round(control_dist_km * 3 + 60)
        return start.shift(minutes=minutes).isoformat()

    # time limits given by https://rusa.org/pages/rulesForRiders?utm_source=chatgpt.com#:~:text=ACP%20Finishing%20Time%20LImits
    if control_dist_km >= brevet_dist_km:
        limits = {
            200: 810,
            300: 1200,
            400: 1620,
            600: 2400,
            1000: 4500
        }
        return start.shift(minutes=limits[brevet_dist_km]).isoformat()

    return calculate_time(control_dist_km, brevet_dist_km, brevet_start_time, 0)



def calculate_time(control_dist_km, brevet_dist_km, brevet_start_time, table_index):

    """
    Args:
        control_dist_km:  number, the control distance in kilometers
        brevet_dist_km: number, the nominal distance of the brevet
            in kilometers, which must be one of 200, 300, 400, 600,
            or 1000 (the only official ACP brevet distances)
        brevet_start_time:  An ISO 8601 format date-time string indicating
            the official start time of the brevet
        table_index: index (0 or 1) of our ACP_MIN_MAX_TABLE key list, so we know
            whether to use min speeds or max speeds
    Returns:
        An ISO 8601 format date string indicating the control open time.
        This will be in the same time zone as the brevet start time.
    """
    
    if control_dist_km > brevet_dist_km: control_dist_km = brevet_dist_km
    
    total_time = arrow.get(brevet_start_time)
    total_hour_shift = 0

    last_control = 0

    for distance in ACP_MIN_MAX_TABLE:

        hours = 0
        local_distance = distance - last_control

        # if we are on the last distance table element before control is reached
        on_last_distance = (control_dist_km > local_distance)
        if (on_last_distance): hours = (local_distance)/ACP_MIN_MAX_TABLE[distance][table_index]
        else: hours = control_dist_km/ACP_MIN_MAX_TABLE[distance][table_index]
        
        # add our hours to the total time
        total_hour_shift += hours
        
        if control_dist_km > local_distance:
            control_dist_km -= (local_distance)
            last_control = distance
        else:
            return total_time.shift(minutes = round(total_hour_shift * 60)).isoformat()
        
    return total_time.shift(minutes = round(total_hour_shift * 60)).isoformat()