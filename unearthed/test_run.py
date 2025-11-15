from pybricks.hubs import PrimeHub
from pybricks.parameters import Axis, Direction, Port, Stop
from pybricks.pupdevices import Motor
from pybricks.robotics import DriveBase
from pybricks.tools import multitask, run_task, wait

from utility import TurnByWheel, EnablePID, DisablePID

# Set up all devices.
prime_hub = PrimeHub(top_side=Axis.Z, front_side=Axis.X)
rightwheel = Motor(Port.C, Direction.CLOCKWISE)
leftwheel = Motor(Port.D, Direction.COUNTERCLOCKWISE)
drive_base = DriveBase(leftwheel, rightwheel, 62.4, 80)
left_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.F, Direction.COUNTERCLOCKWISE)

# Initialize variables.
heading = 0
distance = 0

async def main():
    drive_base.use_gyro(True)
    drive_base.settings(straight_speed=600)
    drive_base.settings(straight_acceleration=300)
    await drive_base.straight(-10)
    await drive_base.straight(750, Stop.COAST)
    await TurnByWheel(prime_hub, drive_base, leftwheel, rightwheel, 90)
    DisablePID(drive_base)
    await drive_base.straight(150)
    print(f"heading after straight {prime_hub.imu.heading()} drive_base angle {drive_base.angle()}")
    EnablePID(drive_base)


run_task(main())