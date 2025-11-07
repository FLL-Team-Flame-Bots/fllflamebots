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
    await motor.run_target(speed, target_angle, Stop.HOLD)
    print(f"run_motor_and_wait angle {motor.angle()}")
    await wait(wait_ms)

async def run_motor_multi_steps(motor, speed, target_angles):
    for target_angle in target_angles:
        await motor.run_target(speed, target_angle)
        await wait(10)
        print(f"Left motor angle {target_angle} {left_motor.angle()}")


async def mission_mineshaft():
    await multitask(
        drive_base.straight(-734),
        # Worm gear can't be reset. The gear's starting position might vary a 
        # bit. Run the motor further, then back, to correct tiny gaps between 
        # gear teeth.
        run_motor_multi_steps(left_motor, 1000, [1200, 650]),
    )
    print(f"Left motor angle {left_motor.angle()}")
    print(f"Right motor angle {right_motor.angle()}")
    print(f"Backup distance {drive_base.distance()}")
    
    await drive_base.turn(-90 - prime_hub.imu.heading())
    await multitask (
        TurnByWheel(prime_hub, drive_base, leftwheel, rightwheel, -90),
        right_motor.run_target(500, -240)
    )
    # Backward drive to mission 03, life both arms to appropriate angle.
    print(f"Heading after -90 turn {prime_hub.imu.heading()}")
    drive_base.settings(straight_speed=200)
    drive_base.settings(straight_acceleration=100)
    start_distance = drive_base.distance()
    # Multitask with timer to avoid stuck at mission #4    
    await multitask(
        drive_base.straight(150),
        wait(3000),
        race=True,
    )
    print(f"Heading after straight 148 {prime_hub.imu.heading()}")
    delta_distance = drive_base.distance() - start_distance
    print(f"Distance toward mission #4 {delta_distance}")
    # Complete mission #4 only if drive base actually moves into position
    if delta_distance > 120:
        await multitask(
            # Life the left arm to pick up artifact
            left_motor.run_target(1000, 1070),
            run_motor_and_wait(right_motor, 150, -115, 500),
        )
        await right_motor.run_target(150, -100)      
    drive_base.settings(straight_speed=600)
    drive_base.settings(straight_acceleration=300)
    # Backoff the same distance as it moved forward to mission #4
    async def backoff_when_stuck():
        await wait(2000)
        await right_motor.run_target(500, 650)
        await drive_base.straight(-170)

    await multitask(
        drive_base.straight(-190),
        backoff_when_stuck(),
        race=True,
    )

async def mission_forum():
    # Return to base, facing 45 degrees
    drive_base.settings(straight_speed=800)
    drive_base.settings(straight_acceleration=1000)
    drive_base.settings(turn_rate=360)
    drive_base.settings(turn_acceleration=360)
    await drive_base.turn(-prime_hub.imu.heading())
    async def return_to_base():
        await drive_base.straight(600)
        await drive_base.turn(45 - prime_hub.imu.heading())
        await drive_base.straight(150)
    
    # Run back to home base, facing 45 degree, wait for items to be put
    # behind.
    await multitask(
        return_to_base(),
        right_motor.run_target(500, 0),
        left_motor.run_target(2000, 1500)
    )    
    # Wait for 2s, place pieces behind robot base.
    await wait(2000)
    drive_base.settings(straight_speed=600)
    drive_base.settings(straight_acceleration=600)
    await drive_base.straight(-430)
    await drive_base.straight(440)


async def main():
    run_watch.reset()
    drive_base.use_gyro(True)
    drive_base.settings(straight_speed=600)
    drive_base.settings(straight_acceleration=300)
    drive_base.settings(turn_rate=90)
    drive_base.settings(turn_acceleration=180)
    async def reset_right_motor():
        await right_motor.run_until_stalled(500, duty_limit=50)
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
    await mission_forum()
    print(f"mineshaft run time {run_watch.time()}")
    print(f"battery {prime_hub.battery.voltage()}")
    drive_base.stop()

run_task(main())
