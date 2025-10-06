from pybricks.hubs import PrimeHub
from pybricks.parameters import Axis, Direction, Port, Stop
from pybricks.pupdevices import Motor
from pybricks.robotics import DriveBase
from pybricks.tools import StopWatch, multitask, run_task, wait

from utility import AccurateTurn

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
    await right_motor.run_angle(speed, angle)
    await wait(wait_ms)


async def run1_mission4():
    global start_distance, delta_distance
    await wait(0)
    # Backward drive to mission 03, life both arms to appropriate angle.
    await multitask(
        left_motor.run_angle(1000, 300),
        right_motor.run_angle(500, 25),
        drive_base.straight(-742),
    )
    print(f"Backup distance {drive_base.distance()}")
    # Left turn toward mission 4, move ahead
    await drive_base.turn(-95 - prime_hub.imu.heading())
    await AccurateTurn(prime_hub, drive_base, -90)
    print(f"Heading after -90 turn {prime_hub.imu.heading()}")
    drive_base.settings(straight_speed=300)
    drive_base.settings(straight_acceleration=100)
    # Previous turn can have errors. Set heading toward -90
    await drive_base.turn(-90 - prime_hub.imu.heading())
    start_distance = drive_base.distance()
    # Multitask with timer to avoid stuck at mission #4
    await multitask(
        # drive_base.straight(152),
        drive_base.straight(148),
        wait(3000),
        race=True,
    )
    delta_distance = drive_base.distance() - start_distance
    print(f"Distance toward mission #4 {delta_distance}")
    # Complete mission #4 only if drive base actually moves into position
    if delta_distance > 120:
        await multitask(
            left_motor.run_angle(500, 850),
            run_motor_and_wait(right_motor, 150, 150, 500),
        )
    drive_base.settings(straight_speed=600)
    drive_base.settings(straight_acceleration=300)
    # Backoff the same distance as it moved forward to mission #4
    await drive_base.straight(-delta_distance + 20)


async def run1_mission13():
    # Orient toward mission #13
    await multitask(
        drive_base.turn(-50 - prime_hub.imu.heading()),
        left_motor.run_angle(1500, 500),
        right_motor.run_angle(1500, -20),
    )
    print(f"Heading after turning to #13 {prime_hub.imu.heading()}")
    await drive_base.straight(430)
    # Lowering left motor so that precious artifact can be dragged by statue.
    await left_motor.run_angle(2000, -1200)
    drive_base.settings(straight_speed=200)
    drive_base.settings(straight_acceleration=100)
    print(f"Heading before dropping artifact {prime_hub.imu.heading()}")
    await drive_base.turn(-45 - prime_hub.imu.heading())
    print(f"Heading after -45 {prime_hub.imu.heading()}")
    await drive_base.straight(-150)
    print(f"Heading after dropping artifact {prime_hub.imu.heading()}")
    drive_base.settings(straight_speed=600)
    drive_base.settings(straight_acceleration=300)
    # Move toward mission #13 again trying to lift statue
    await multitask(
        right_motor.run_angle(1500, -right_motor.angle()),
        left_motor.run_angle(4000, 1000),
    )
    print(f"Heading toward mission 13 {prime_hub.imu.heading()}")

    # Multitask with timer to avoid stuck at mission #13
    async def lift_statue():
        print(f"Right motor angle before lifting {right_motor.angle()}")
        await AccurateTurn(prime_hub, drive_base, -55, adjust_factor=1.2)
        print(f"Heading toward statue {prime_hub.imu.heading()}")
        await drive_base.straight(100)
        print(f"Heading before lifting {prime_hub.imu.heading()}")
        await multitask(
            right_motor.run_angle(500, 45 - right_motor.angle()),
            left_motor.run_angle(1000, -900),
        )
        await drive_base.turn(-80 - prime_hub.imu.heading())
        await wait(500)

    await multitask(
        lift_statue(),
        wait(5000),
        race=True,
    )
    drive_base.settings(straight_speed=600)
    drive_base.settings(straight_acceleration=300)
    await drive_base.turn(-60 - prime_hub.imu.heading())
    # await drive_base.straight(-300)
    await multitask(
        drive_base.straight(-300),
        right_motor.run_angle(300, 200 - right_motor.angle()),
        left_motor.run_angle(5000, 1000),
    )


async def main():
    run_watch.reset()
    right_motor.reset_angle(0)
    left_motor.reset_angle(0)
    drive_base.use_gyro(True)
    drive_base.settings(straight_speed=600)
    drive_base.settings(straight_acceleration=150)
    drive_base.settings(turn_rate=90)
    drive_base.settings(turn_acceleration=180)
    mission_watch.reset()
    await run1_mission4()
    print(["mission4 time", mission_watch.time()])
    mission_watch.reset()
    await run1_mission13()
    print(["mission13 time", mission_watch.time()])
    drive_base.settings(straight_speed=1000)
    drive_base.settings(straight_acceleration=500)
    drive_base.settings(turn_rate=360)
    drive_base.settings(turn_acceleration=180)
    await drive_base.turn(15 - prime_hub.imu.heading())
    print(f"Heading before exiting {prime_hub.imu.heading()}")
    await drive_base.straight(700)
    print(["Run1 time", run_watch.time()])


run_task(main())
