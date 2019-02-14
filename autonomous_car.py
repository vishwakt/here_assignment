import collections
import logging

ModeToSpeed = collections.namedtuple(
    'ModeToSpeed', ('description', 'normal', 'sport', 'safe'))

DefaultEventDataMap = {
    1: ModeToSpeed(description='Traffic', normal=-10, sport=-5, safe=-15),
    2: ModeToSpeed(description='Traffic Clear', normal=10, sport=5, safe=15),
    3: ModeToSpeed(description='Weather Rainy', normal=-5, sport=-5, safe=-5),
    4: ModeToSpeed(description='Weather Clear', normal=5, sport=5, safe=5),
    5: ModeToSpeed(description='Slippery Road', normal=-15, sport=-15, safe=-15),
    6: ModeToSpeed(description='Slippery Road Clear', normal=15, sport=15, safe=15),
    7: ModeToSpeed(description='Emergency Turbo', normal=20, sport=30, safe=10),
    10: ModeToSpeed(description='Speed Limit Sign X', normal=0, sport=5, safe=-5)
}


class UnknownModeError(Exception):
    """Raised when mode is Unknown."""
    pass


class AutonomousCar(object):
    """An Autonomous car class that changes speed of the car
    according to speed limit signs, road & weather conditions"""

    def __init__(self, mode, speed=20, event_data_map=DefaultEventDataMap, min_speed=10):
        """Constructor for a Car object

        Args:
            mode: Drive mode.
            speed: Initial speed set to 20kph.
            event_data_map: A collections object containing road conditions and relevant speeds.
            min_speed: Minimum allowed vehicle speed.
        """
        self._mode = mode
        self._speed = speed
        self._event_data_map = event_data_map
        self._min_speed = min_speed
        self._past_events = {}
        self._emergency_turbo_used = False
        logging.debug('Speed: %s', self._speed)

    def _set_speed(self, speed):
        if speed >= self._min_speed:
            self._speed = speed
        logging.debug('Speed: %s', self._speed)

    def _get_speed(self):
        return self._speed

    def _add_event_in_past_events(self, event_id):
        """Add event into past events list to avoid calling same event twice."""
        self._past_events[event_id] = True

    def _clear_event_in_past_events(self, event_id):
        """Clear event if weather or road conditions are favorable."""
        self._past_events.pop(event_id, None)

    def _update_speed(self, event_id):
        """Update vehicle speed after incrementing or decrementing."""
        speed_delta = getattr(self._event_data_map[event_id], self._mode)
        new_speed = self._get_speed() + speed_delta
        self._set_speed(new_speed)

    def _traffic(self):
        """Sensor event indicating high traffic."""
        if 1 in self._past_events:
            return
        self._update_speed(1)
        self._add_event_in_past_events(1)
        self._clear_event_in_past_events(2)

    def _traffic_clear(self):
        """Sensor event indicating reduced traffic."""
        if 2 in self._past_events or 1 not in self._past_events:
            return
        self._update_speed(2)
        self._add_event_in_past_events(2)
        self._clear_event_in_past_events(1)

    def _weather_rainy(self):
        """Sensor event indicating rainy weather conditions."""
        if 3 in self._past_events:
            return
        self._update_speed(3)
        self._add_event_in_past_events(3)
        self._clear_event_in_past_events(4)

    def _weather_clear(self):
        """Sensor event indicating clear skies."""
        if 4 in self._past_events or 3 not in self._past_events:
            return
        self._update_speed(4)
        self._add_event_in_past_events(4)
        self._clear_event_in_past_events(3)

    def _slippery_road(self):
        """Sensor event indicating slippery conditions."""
        if 5 in self._past_events:
            return
        self._update_speed(5)
        self._add_event_in_past_events(5)
        self._clear_event_in_past_events(6)

    def _slippery_road_clear(self):
        """Sensor event indicating road favorable for higher speed."""
        if 6 in self._past_events or 5 not in self._past_events:
            return
        self._update_speed(6)
        self._add_event_in_past_events(6)
        self._clear_event_in_past_events(5)

    def _emergency_turbo(self):
        """Sensor event indicating Emergency turbo."""
        if not self._emergency_turbo_used and 5 not in self._past_events:
            self._update_speed(7)
            self._emergency_turbo_used = True
            self._add_event_in_past_events(7)

    def _speed_limit_sign(self, speed):
        """Sensor event indicating Speed Limit sign."""
        speed_delta = getattr(self._event_data_map[10], self._mode)
        new_speed = speed + speed_delta
        self._set_speed(new_speed)
        self._clear_event_in_past_events(7)

    def observe(self, event_id):
        """Function to call different sensor events according to the sensor ID."""
        if event_id > 100 and event_id not in self._event_data_map.keys():
            return
        elif event_id >= 10:
            self._speed_limit_sign(event_id)
        elif event_id == 7:
            self._emergency_turbo()
        elif event_id == 6:
            self._slippery_road_clear()
        elif event_id == 5:
            self._slippery_road()
        elif event_id == 4:
            self._weather_clear()
        elif event_id == 3:
            self._weather_rainy()
        elif event_id == 2:
            self._traffic_clear()
        elif event_id == 1:
            self._traffic()


def main():
    mode = raw_input('Enter mode(NORMAL, SPORT or SAFE): ').lower()
    if mode not in ('normal', 'sport', 'safe'):
        raise UnknownModeError()
    car = AutonomousCar(mode)
    while True:
        event_id = int(raw_input('Enter Event: '))
        car.observe(event_id)


if __name__ == '__main__':
    # Please comment out the below line before using in production!!!
    logging.basicConfig(level=logging.DEBUG)
    main()
