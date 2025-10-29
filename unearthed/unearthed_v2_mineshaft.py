from pybricks.hubs import PrimeHub
from pybricks.parameters import Axis, Direction, Port, Stop
from pybricks.pupdevices import Motor
from pybricks.robotics import DriveBase
from pybricks.tools import StopWatch, multitask, run_task, wait

from utility import TurnByWheel

# Set up all devices.
prime_hub = PrimeHub(top_side=Axis.Z, front_side=Axis.X)
run_watch = StopWatch()
mission_watch = StopWatch()
rightwheel = Motor(Port.C, Direction.CLOCKWISE)
leftwheel = Motor(Port.D, Direction.COUNTERCLOCKWISE)
drive_base = DriveBase(leftwheel, rightwheel, 62.4, 80)
left_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.F, Direction.COUNTERCLOCKWISE)

# Initialize variables.
heading = 0


async def run_motor_and_wait(motor, speed, target_angle, wait_ms):
    await motor.run_target(speed, target_angle)
    await wait(wait_ms)


async def mission_mineshaft():
    await multitask(
        drive_base.straight(-742),
        left_motor.run_target(500, 650)
    )
    print(f"Left motor angle {left_motor.angle()}")
    print(f"Right motor angle {right_motor.angle()}")
    print(f"Backup distance {drive_base.distance()}")
    
    await drive_base.turn(-90 - prime_hub.imu.heading())
    await TurnByWheel(prime_hub, drive_base, leftwheel, rightwheel, -90)
    await right_motor.run_target(500, -190)
    # Backward drive to mission 03, life both arms to appropriate angle.
    print(f"Heading after -90 turn {prime_hub.imu.heading()}")
    drive_base.settings(straight_speed=300)
    drive_base.settings(straight_acceleration=100)
    start_distance = drive_base.distance()
    # Multitask with timer to avoid stuck at mission #4
    await multitask(
        drive_base.straight(160),
        wait(3000),
        race=True,
    )
    print(f"Heading after straight 148 {prime_hub.imu.heading()}")
    delta_distance = drive_base.distance() - start_distance
    print(f"Distance toward mission #4 {delta_distance}")
    # Complete mission #4 only if drive base actually moves into position
    if delta_distance > 120:
        await multitask(
            left_motor.run_target(500, 1050),
            run_motor_and_wait(right_motor, 150, -40, 500),
        )
    drive_base.settings(straight_speed=600)
    drive_base.settings(straight_acceleration=300)
    # Backoff the same distance as it moved forward to mission #4
    await drive_base.straight(-delta_distance)


# async def mission_forum():
#     # Orient toward mission #13
#     await multitask(
#         drive_base.turn(-40 - prime_hub.imu.heading()),
#         #left_motor.run_target(500, 500),
#         right_motor.run_target(500, 0),
#     )
#     left_motor.run_target(500, 0),
#     drive_base.settings(straight_speed=1000)
#     drive_base.settings(straight_acceleration=1000)
#     print(f"Heading after turning to #13 {prime_hub.imu.heading()}")
#     await drive_base.straight(250, Stop.BRAKE)
#     drive_base.settings(turn_rate=360)
#     drive_base.settings(turn_acceleration=750)
#     await drive_base.turn(45)


async def main():
    run_watch.reset()
    drive_base.use_gyro(True)
    drive_base.settings(straight_speed=600)
    drive_base.settings(straight_acceleration=150)
    drive_base.settings(turn_rate=90)
    drive_base.settings(turn_acceleration=180)
    async def reset_right_motor():
        right_motor.run_until_stalled(500, duty_limit=50)
        right_motor.reset_angle(0)

    async def reset_left_motor():
        left_motor.reset_angle(0)
        #left_motor.run_target(500, 650)

    await multitask(
        drive_base.straight(10),
        reset_right_motor(),
        reset_left_motor()
    )
    
    drive_base.reset(0, 0)
    await mission_mineshaft()
    drive_base.settings(straight_speed=800)
    drive_base.settings(straight_acceleration=1000)
    await drive_base.turn(5 - prime_hub.imu.heading())
    await multitask(
        drive_base.straight(750),
        right_motor.run_target(500, 0)
    )
    # await mission_forum()
    print(f"mineshaft run time {run_watch.time()}")
    # print(f"battery {prime_hub.battery.voltage()}")
    drive_base.stop()
    


run_task(main())
