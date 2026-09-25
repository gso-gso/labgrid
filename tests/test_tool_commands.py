from unittest.mock import Mock, patch

from labgrid.driver.adb import ADBDriver
from labgrid.driver.openocddriver import OpenOCDDriver
from labgrid.resource.adb import USBADBDevice


def test_adb_command_prefix():
    driver = ADBDriver.__new__(ADBDriver)
    driver.tool = ["env", "ADB_TRACE=1", "adb"]
    driver.device = USBADBDevice(None, None, "serial")
    driver.on_activate()

    assert driver._base_command == ["env", "ADB_TRACE=1", "adb", "-s", "serial"]


def test_openocd_command_prefix():
    driver = OpenOCDDriver.__new__(OpenOCDDriver)
    driver.tool = ["podman", "exec", "tools", "openocd"]
    driver.search = []
    driver.config = []
    driver.interface_config = None
    driver.board_config = None
    driver.interface = Mock(path="1-2.3")
    driver.interface.wrap_command.side_effect = lambda command: command

    with patch("labgrid.driver.openocddriver.processwrapper.check_output") as run:
        driver._run_commands(["shutdown"])

    assert run.call_args.args[0][:4] == ["podman", "exec", "tools", "openocd"]
