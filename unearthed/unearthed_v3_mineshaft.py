from pybricks.hubs import PrimeHub
from pybricks.parameters import Axis, Direction, Port, Stop
from pybricks.pupdevices import Motor
from pybricks.robotics import DriveBase
from pybricks.tools import StopWatch, multitask, run_task, wait

from utility import turn_by_wheel, straight_at_speed

# Set up all devices.
prime_hub = PrimeHub(top_side=Axis.Z, front_side=Axis.X)
watch = StopWatch()
rightwheel = Motor(Port.C, Direction.CLOCKWISE)
leftwheel = Motor(Port.D, Direction.COUNTERCLOCKWISE)
drive_base = DriveBase(leftwheel, rightwheel, 62.4, 114)
left_motor = Motor(Port.B, Direction.CLOCKWISE)
right_motor = Motor(Port.F, Direction.COUNTERCLOCKWISE)


async def reset_left_motor():
    await left_motor.run_until_stalled(500, Stop.HOLD, 50)
    left_motor.reset_angle(0)


async def reset_right_motor():
    await right_motor.run_until_stalled(500, Stop.HOLD, 50)
    right_motor.reset_angle(0)


async def reset_base():
    await drive_base.straight(-10)
    drive_base.reset(0, 0)
    drive_base.use_gyro(True)


async def main():
    watch.reset()
    print("Battery", prime_hub.battery.voltage(), sep=", ")
    await multitask(
        reset_left_motor(),
        reset_right_motor(),
        reset_base(),
    )
    drive_base.settings(straight_speed=600)
    drive_base.settings(straight_acceleration=300)
    drive_base.settings(turn_rate=100)
    await drive_base.straight(730)
    await turn_by_wheel(prime_hub, drive_base, leftwheel, rightwheel, 90)
    await straight_at_speed(drive_base, 120, speed=300, acceleration=200)
    # drop flag
    await right_motor.run_angle(300, -200)
    await straight_at_speed(drive_base, 175, speed=300, acceleration=200)
    
    # Face mission 4, back up a bit, drop right arm all the way down.
    await turn_by_wheel(prime_hub, drive_base, leftwheel, rightwheel, 0)
    await drive_base.straight(-135)
    await right_motor.run_until_stalled(-300, Stop.HOLD, 50)
    print(f"heading after backoff {prime_hub.imu.heading()}")
    # Move toward mission 4, raise right arm to lift mineshaft, then
    # move and continue lifting mineshaft.
    await drive_base.straight(50)
    await turn_by_wheel(prime_hub, drive_base, leftwheel, rightwheel, 0)
    print(f"heading toward mission 4 {prime_hub.imu.heading()}")
    await right_motor.run_angle(300, 100)
    await multitask(
        straight_at_speed(drive_base, 120, speed=200, acceleration=200),
        right_motor.run_angle(140, 80),
    )
    await wait(100)

    # Lower left arm to pick up artifact.
    await multitask(
        wait(2000),
        left_motor.run_until_stalled(-500, Stop.HOLD, 80),
        # left_motor.run_angle(1000, -290),
        race=True,
    )
    await left_motor.run_angle(150, 270)
    # Back off, turn -180 toward forum
    await multitask(
        drive_base.straight(-90), right_motor.run_until_stalled(500, Stop.HOLD, 50)
    )
    await drive_base.turn(-180)
    await left_motor.run_target(-1000, -150)
    await left_motor.run_until_stalled(1000, Stop.HOLD, 50)
    # await left_motor.run_angle(1000, 100)
    await drive_base.straight(-70)
    await drive_base.turn(prime_hub.imu.heading() + 65)
    await turn_by_wheel(prime_hub, drive_base, leftwheel, rightwheel, -295)
    print(f"heading toward last flag {prime_hub.imu.heading()}")
    await drive_base.straight(460)
    print(f"heading delivered last flag {prime_hub.imu.heading()}")
    print("Total time (ms):", watch.time())


run_task(main())
