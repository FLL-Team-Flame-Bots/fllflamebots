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
        left_motor.run_angle(1000, 400),
        right_motor.run_angle(500, 30),
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
        drive_base.straight(152),
        wait(3000),
        race=True,
    )
    delta_distance = drive_base.distance() - start_distance
    # Complete mission #4 only if drive base actually moves into position
    if delta_distance > 120:
        await multitask(
            left_motor.run_angle(500, 650),
            run_motor_and_wait(right_motor, 200, 150, 500),
        )
    drive_base.settings(straight_speed=600)
    drive_base.settings(straight_acceleration=300)
    # Backoff the same distance as it moved forward to mission #4
    await drive_base.straight(-delta_distance)


async def run1_mission2():
    await wait(0)
    # Speed up to reach mission #2 in time
    drive_base.settings(straight_speed=1000)
    drive_base.settings(straight_acceleration=500)
    drive_base.settings(turn_rate=90)
    drive_base.settings(turn_acceleration=180)
    # In parallel, move backward toward mission #2, and lift right arm toward back
    await multitask(
        drive_base.turn(-40 - prime_hub.imu.heading()),
        # Lift right arm all the way toward back. Set a timer to avoid stuck.
        multitask(
            right_motor.run_angle(300, 350),
            wait(2000),
            race=True,
        ),
    )
    await drive_base.straight(-300)
    await right_motor.run_angle(300, -200)


async def run1_mission13():
    # Orient toward mission #13
    await multitask(
        drive_base.turn(-53 - prime_hub.imu.heading()),
        left_motor.run_angle(1500, 500),
        right_motor.run_angle(1500, 30),
    )
    print(f"Heading after turning to #13 {prime_hub.imu.heading()}")
    await drive_base.straight(430)
    # Lowering left motor so that precious artifact can be dragged by statue.
    await left_motor.run_angle(2000, -1200, Stop.COAST)
    await drive_base.straight(-120, then=Stop.COAST)
    # Move toward mission #13 again trying to lift statue
    await multitask(
        # drive_base.turn(-60 - prime_hub.imu.heading()),
        right_motor.run_angle(1500, -200),
        left_motor.run_angle(4000, 1000, Stop.COAST),
    )
    print(f"Heading toward mission 13 {prime_hub.imu.heading()}")

    # Multitask with timer to avoid stuck at mission #13
    async def lift_statue():
        await drive_base.straight(80)
        await right_motor.run_angle(500, 30)
        await drive_base.turn(-75 - prime_hub.imu.heading())
        await drive_base.straight(10)
        await run_motor_and_wait(right_motor, 500, 50, 500)

    await multitask(
        lift_statue(),
        wait(5000),
        race=True,
    )
    await drive_base.straight(-200)


async def main():
    run_watch.reset()
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
    mission_watch.reset()
    await run1_mission2()
    print(["mission2 time", mission_watch.time()])
    # Leave mission 2, go back
    await drive_base.straight(40)
    await drive_base.turn(50, then=Stop.COAST)
    drive_base.settings(straight_speed=1000)
    drive_base.settings(straight_acceleration=500)
    await drive_base.straight(800)
    print(["Run1 time", run_watch.time()])


run_task(main())
