from pybricks.hubs import PrimeHub
from pybricks.parameters import Axis, Direction, Port, Stop
from pybricks.pupdevices import Motor
from pybricks.robotics import DriveBase
from pybricks.tools import StopWatch, multitask, run_task, wait

from utility import TurnByWheel, StraightAtSpeed

# Set up all devices.
prime_hub = PrimeHub(top_side=Axis.Z, front_side=Axis.X)
watch = StopWatch()
rightwheel = Motor(Port.C, Direction.CLOCKWISE)
leftwheel = Motor(Port.D, Direction.COUNTERCLOCKWISE)
drive_base = DriveBase(leftwheel, rightwheel, 62.4, 114)
left_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.F, Direction.COUNTERCLOCKWISE)

async def subtask():
    await left_motor.run_until_stalled(-500, Stop.HOLD, 50)
    left_motor.reset_angle(0)

async def subtask2():
    await right_motor.run_until_stalled(500, Stop.HOLD, 50)
    right_motor.reset_angle(0)

async def subtask3():
    await drive_base.straight(-10)
    drive_base.reset(0, 0)
    drive_base.use_gyro(True)






async def main():
    watch.reset()
    print('Battery', prime_hub.battery.voltage(), sep=", ")
    await multitask(
        subtask(),
        subtask2(),
        subtask3(),
    )
    drive_base.settings(straight_speed=600)
    drive_base.settings(straight_acceleration=300)
    drive_base.settings(turn_rate=100)
    await drive_base.straight(735)
    await drive_base.turn(90)
    await TurnByWheel(prime_hub, drive_base, leftwheel, rightwheel, 90)
    await drive_base.straight(120)
    #drop flag
    await right_motor.run_angle(150, -200)
    await drive_base.straight(175)
    await drive_base.turn(-90)
    await TurnByWheel(prime_hub, drive_base, leftwheel, rightwheel, 0)
    
    await drive_base.straight(-135)
    await TurnByWheel(prime_hub, drive_base, leftwheel, rightwheel, 0)
    await right_motor.run_until_stalled(-300, Stop.HOLD, 50)
    
    
    await drive_base.straight(40)
    await right_motor.run_angle(300, 100)
    await multitask(
        StraightAtSpeed(drive_base, 130, speed=200, acceleration=200),
        right_motor.run_angle(140, 80),
    )
    await wait(100)

    await multitask(
        wait(2000),
        left_motor.run_angle(150, 300),
        race =True, 
    )
    await left_motor.run_angle(150, -280)
    #back away
    await multitask(
        drive_base.straight(-90),
        right_motor.run_until_stalled(500, Stop.HOLD, 50)
    )
    await drive_base.turn(-180)
    await left_motor.run_until_stalled(500, Stop.HOLD, 50)
    await left_motor.run_angle(500, -300)
    await drive_base.straight(-50)
    await drive_base.turn(-135)
    await drive_base.straight(700)


run_task(main())