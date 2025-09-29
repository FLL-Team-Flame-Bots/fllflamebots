from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

hub = PrimeHub()
from pybricks.tools import hub_menu

# Based on the selection, run a program.
while True:
    # Make a menu to choose a letter. You can also use numbers.
    selected = hub_menu("1", "2", "3", "4", "5", "6", "7")
    # Based on the selection, run a program.
    if selected == "1":
        import unearthed_run1
    elif selected == "2":
        import unearthed_run2
    elif selected == "3":
        import unearthed_run3
    elif selected == "4":
        import unearthed_run4
    elif selected == "5":
        import unearthed_run5
    elif selected == "6":
        import unearthed_run6
    elif selected == "7":
        import unearthed_run7




