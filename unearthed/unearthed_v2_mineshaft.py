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


async def run_motor_and_wait(motor, speed, angle, wait_ms):
    await motor.run_angle(speed, angle)
    await wait(wait_ms)


async def mission_mineshaft():
    await drive_base.straight(-742)
    await drive_base.turn(-90 - prime_hub.imu.heading())
    await TurnByWheel(prime_hub, drive_base, leftwheel, rightwheel, -90)
    # Backward drive to mission 03, life both arms to appropriate angle.
    await multitask(
        #left_motor.run_target(500, 0),
        left_motor.run_until_stalled(-500, duty_limit=50),
        right_motor.run_target(500, -200)
    )
    print(f"Left motor angle {left_motor.angle()}")
    print(f"Backup distance {drive_base.distance()}")
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
            left_motor.run_target(500, 45),
            run_motor_and_wait(right_motor, 150, 150, 500),
        )
    drive_base.settings(straight_speed=600)
    drive_base.settings(straight_acceleration=300)
    # Backoff the same distance as it moved forward to mission #4
    await drive_base.straight(-delta_distance + 20)


async def mission_forum():
    # Orient toward mission #13
    await multitask(
        drive_base.turn(-50 - prime_hub.imu.heading()),
        #left_motor.run_target(500, 500),
        right_motor.run_target(500, 0),
    )
    left_motor.run_target(500, 0),
    drive_base.settings(straight_speed=1000)
    drive_base.settings(straight_acceleration=1000)
    print(f"Heading after turning to #13 {prime_hub.imu.heading()}")
    await drive_base.straight(250)


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
        left_motor.run_until_stalled(-500, duty_limit=50)
        left_motor.reset_angle(0)
        left_motor.run_target(500, 180)

    await multitask(
        drive_base.straight(10),
        reset_right_motor(),
        reset_left_motor()
    )
    
    drive_base.reset(0, 0)
    mission_watch.reset()
    await mission_mineshaft()
    print(["mission4 time", mission_watch.time()])
    mission_watch.reset()
    await mission_forum()
    print(["mission_forum time", mission_watch.time()])
    drive_base.settings(straight_speed=1000)
    drive_base.settings(straight_acceleration=500)
    drive_base.settings(turn_rate=360)
    drive_base.settings(turn_acceleration=180)
    await drive_base.turn(15 - prime_hub.imu.heading())
    print(f"Heading before exiting {prime_hub.imu.heading()}")
    await drive_base.straight(700)
    print(["Run1 time", run_watch.time()])
    print(f"battery {prime_hub.battery.voltage()}")
    drive_base.use_gyro(False)
    drive_base.stop()
    


run_task(main())
