import unittest
from autonomous_car import AutonomousCar


class TestAutonomousCar(unittest.TestCase):
    def setUp(self):
        self.car = AutonomousCar('normal')

    def test_set_speed(self):
        self.car._set_speed(5)
        self.assertEqual(20, self.car._speed)
        self.car._set_speed(11)
        self.assertEqual(11, self.car._speed)
        self.car._set_speed(100)
        self.assertNotEqual(20, self.car._speed)
        self.car._set_speed(200)
        self.assertNotEqual(20, self.car._speed)

    def test_get_speed(self):
        self.car._get_speed()
        self.assertEqual(20, self.car._speed)
        self.car._set_speed(45)
        self.assertEqual(45, self.car._get_speed())

    def test_add_event_in_past_events(self):
        self.car._add_event_in_past_events(1)
        self.assertEqual({1: True}, self.car._past_events)
        self.car._add_event_in_past_events(1)
        self.assertNotEqual({2: True}, self.car._past_events)
        self.car._add_event_in_past_events(3)
        self.assertEqual({1: True, 3: True}, self.car._past_events)
        self.car._add_event_in_past_events(6)
        self.assertEqual({1: True, 3: True, 6: True}, self.car._past_events)
        self.car._add_event_in_past_events(1)
        self.assertEqual({1: True, 3: True, 6: True}, self.car._past_events)

    def _clear_event_in_past_events(self):
        self.car._clear_event_in_past_events()
        self.assertEqual({}, self.car._past_events)

    def test_traffic(self):
        self.car._traffic()
        self.assertEqual(10, self.car._speed)
        self.assertEqual({1: True}, self.car._past_events)
        self.car._clear_event_in_past_events(1)
        self.car._set_speed(45)
        self.car._traffic()
        self.assertEqual(35, self.car._speed)
        self.assertEqual({1: True}, self.car._past_events)
        self.car._clear_event_in_past_events(1)
        self.car._set_speed(55)
        self.car._traffic()
        self.assertEqual(45, self.car._speed)
        self.assertEqual({1: True}, self.car._past_events)
        self.car._clear_event_in_past_events(1)

    def test_traffic_clear(self):
        self.car._set_speed(50)
        self.car._traffic()
        self.car._traffic_clear()
        self.assertEqual(50, self.car._speed)
        self.assertEqual({2: True}, self.car._past_events)
        self.car._clear_event_in_past_events(2)

    def test_weather_rainy(self):
        self.car._weather_rainy()
        self.assertEqual(15, self.car._speed)
        self.assertEqual({3: True}, self.car._past_events)
        self.car._clear_event_in_past_events(3)
        self.car._set_speed(70)
        self.car._weather_rainy()
        self.assertEqual(65, self.car._speed)
        self.assertEqual({3: True}, self.car._past_events)

    def test_weather_clear(self):
        self.car._set_speed(70)
        self.car._weather_rainy()
        self.assertEqual(65, self.car._speed)
        self.car._weather_clear()
        self.assertEqual({4: True}, self.car._past_events)

    def test_slippery_road(self):
        self.car._set_speed(80)
        self.car._slippery_road()
        self.assertEqual(65, self.car._speed)
        self.assertEqual({5: True}, self.car._past_events)

    def test_slippery_road_clear(self):
        self.car._slippery_road()
        self.car._set_speed(80)
        self.car._slippery_road_clear()
        self.assertEqual(95, self.car._speed)
        self.assertEqual({6: True}, self.car._past_events)

    def emergency_turbo(self):
        self.car._emergency_turbo()
        self.assertEqual(35, self.car._speed)
        self.assertEqual(True, self.car._emergency_turbo_used)
        self._emergency_turbo_used = False
        self.car._set_speed(80)
        self.car._slippery_road()
        self.car._emergency_turbo()
        self.assertEqual(65, self.car._speed)
        self.assertEqual({6: True, 7: True}, self.car._past_events)

    def test_observe_event1(self):
        self.car.observe(50)
        self.assertEqual(50, self.car._speed)
        self.car.observe(1)
        self.assertEqual(40, self.car._speed)
        self.assertEqual({1: True}, self.car._past_events)
        self.car.observe(7)
        self.car.observe(60)
        self.car.observe(7)
        self.assertEqual(60, self.car._speed)
        self.car.observe(3)
        self.assertEqual(55, self.car._speed)
        self.assertEqual({1: True, 3: True}, self.car._past_events)
        self.car.observe(5)
        self.assertEqual(40, self.car._speed)
        self.assertEqual({1: True, 3: True, 5: True}, self.car._past_events)
        self.car.observe(2)
        self.assertEqual(50, self.car._speed)
        self.assertEqual({2: True, 3: True, 5: True}, self.car._past_events)
        self.car.observe(4)
        self.assertEqual(55, self.car._speed)
        self.assertEqual({2: True, 4: True, 5: True}, self.car._past_events)
        self.car.observe(6)
        self.assertEqual(70, self.car._speed)
        self.assertEqual({2: True, 4: True, 6: True}, self.car._past_events)
        self.assertEqual(True, self.car._emergency_turbo_used)
        self.car.observe(75)
        self.assertEqual(75, self.car._speed)
        self.car.observe(50)
        self.assertEqual(50, self.car._speed)
        self.car.observe(100)
        self.assertEqual(100, self.car._speed)
        self.car.observe(101)
        self.assertNotEqual(101, self.car._speed)
        self.car.observe(0)
        self.assertEqual(100, self.car._speed)

if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAutonomousCar)
    unittest.TextTestRunner(verbosity=2).run(suite)