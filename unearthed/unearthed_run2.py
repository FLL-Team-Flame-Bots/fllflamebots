from pybricks.hubs import PrimeHub
from pybricks.parameters import Axis, Direction, Port, Stop
from pybricks.pupdevices import Motor
from pybricks.robotics import DriveBase
from pybricks.tools import StopWatch, multitask, run_task, wait

# Set up all devices.
prime_hub = PrimeHub(top_side=Axis.Z, front_side=Axis.X)
stopwatch = StopWatch()
leftwheel = Motor(Port.D, Direction.COUNTERCLOCKWISE)
rightwheel = Motor(Port.C, Direction.CLOCKWISE)
leftattachment = Motor(Port.B, Direction.COUNTERCLOCKWISE)
rightattachment = Motor(Port.F, Direction.COUNTERCLOCKWISE)
drive_base = DriveBase(leftwheel, rightwheel, 62.4, 80)

async def subtask():
    await wait(500)
    for item in [0, 0, 0, 15]:
        await wait(0)
        await prime_hub.speaker.beep(500 + 10 * item, 150 + 15 * item)
        await wait(50)

async def main():
    drive_base.use_gyro(True)
    stopwatch.reset()
    await drive_base.straight(658)
    await drive_base.turn(-95)
    await drive_base.straight(90)
    await multitask(
        leftattachment.run_angle(750, 1100),
        wait(3000),
        race=True,
    )
    await leftattachment.run_angle(600, -1100)
    await drive_base.straight(-100)
    await drive_base.turn(54)
    await multitask(
        drive_base.straight(255),
        wait(3000),
        race=True,
    )
    await multitask(
        drive_base.straight(-250),
        rightattachment.run_angle(500, 90),
    )
    await drive_base.turn(60)
    drive_base.settings(straight_speed=750)
    await multitask(
        drive_base.straight(-700),
        subtask(),
    )
    print(stopwatch.time())
    drive_base.use_gyro(False)
    drive_base.stop()


run_task(main())
