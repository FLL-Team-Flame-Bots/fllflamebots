from pybricks.hubs import PrimeHub
from pybricks.parameters import Axis, Direction, Port, Stop
from pybricks.pupdevices import Motor
from pybricks.robotics import DriveBase
from pybricks.tools import StopWatch, multitask, run_task, wait

# Set up all devices.
prime_hub = PrimeHub(top_side=Axis.Z, front_side=Axis.X)
run_watch = StopWatch()
mission_watch = StopWatch()
rightwheel = Motor(Port.C, Direction.CLOCKWISE)
leftwheel = Motor(Port.D, Direction.COUNTERCLOCKWISE)
drive_base = DriveBase(leftwheel, rightwheel, 62.4, 80)
left_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.F, Direction.COUNTERCLOCKWISE)

async def main():
    run_watch.reset()
    drive_base.use_gyro(True)
    drive_base.settings(straight_speed=1000)
    drive_base.settings(straight_acceleration=1000)
    await drive_base.straight(-400)
    await drive_base.straight(100)
    print(f"final run time {run_watch.time()}")
    drive_base.stop()

run_task(main())
