import pytest
from air_traffic_control import air_traffic_control

class TestAirTrafficControl:

    def test_cacc_runway_clear(self, capsys):
        # Clause: runway_clear in runway_available
        assert air_traffic_control(True, False, 100, False, 20, 2000, 2, False) == "Landing Allowed"
        out, err = capsys.readouterr()
        assert "Debug Info:\nAll conditions met for landing.\n\n" == out

        assert air_traffic_control(False, False, 100, False, 20, 2000, 2, False) == "Landing Denied"
        out, err = capsys.readouterr()
        assert "Debug Info:\nConditions not met for safe landing.\n\n" == out


    def test_cacc_plane_speed(self, capsys):
        # Clause: plane_speed in safe_speed
        assert air_traffic_control(True, False, 120, False, 20, 2000, 2, False) == "Landing Allowed"
        out, err = capsys.readouterr()
        assert "Debug Info:\nAll conditions met for landing.\n\n" == out

        assert air_traffic_control(True, False, 160, False, 20, 2000, 2, False) == "Landing Denied"
        out, err = capsys.readouterr()
        assert "Debug Info:\nConditions not met for safe landing.\n\n" == out


    def test_cacc_airport_traffic(self, capsys):
        # Clause: airport_traffic in acceptable_traffic
        assert air_traffic_control(True, False, 100, False, 20, 2000, 4, False) == "Landing Allowed"
        out, err = capsys.readouterr()
        assert "Debug Info:\nAll conditions met for landing.\n\n" == out

        assert air_traffic_control(True, False, 100, False, 20, 2000, 6, False) == "Landing Denied"
        out, err = capsys.readouterr()
        assert "Debug Info:\nConditions not met for safe landing.\n\n" == out


    def test_inactive_wind_speed(self, capsys):
        # wind_speed is inactive when visibility is low
        assert air_traffic_control(True, False, 100, False, 20, 500, 2, False) == "Landing Denied"
        out, err = capsys.readouterr()
        assert "Debug Info:\nConditions not met for safe landing.\n\n" == out

        assert air_traffic_control(True, False, 100, False, 50, 500, 2, False) == "Landing Denied"
        out, err = capsys.readouterr()
        assert "Debug Info:\nConditions not met for safe landing.\n\n" == out


    def test_inactive_visibility(self, capsys):
        # airport_traffic is inactive when priority_status is False
        assert air_traffic_control(True, False, 100, False, 50, 500, 2, False) == "Landing Denied"
        out, err = capsys.readouterr()
        assert "Debug Info:\nConditions not met for safe landing.\n\n" == out

        assert air_traffic_control(True, False, 100, False, 50, 500, 10, False) == "Landing Denied"
        out, err = capsys.readouterr()
        assert "Debug Info:\nConditions not met for safe landing.\n\n" == out




