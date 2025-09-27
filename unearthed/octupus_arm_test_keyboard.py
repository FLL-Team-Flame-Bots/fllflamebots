from pybricks.hubs import PrimeHub
from pybricks.parameters import Axis, Direction, Port, Stop
from pybricks.pupdevices import Motor
from pybricks.robotics import DriveBase
from pybricks.tools import multitask, run_task, wait
from usys import stdin
from uselect import poll

# Register the standard input so we can read keyboard presses.
keyboard = poll()
keyboard.register(stdin)

# Set up all devices.
prime_hub = PrimeHub(top_side=Axis.Z, front_side=Axis.X)
rightwheel = Motor(Port.C, Direction.CLOCKWISE)
leftwheel = Motor(Port.D, Direction.COUNTERCLOCKWISE)
drive_base = DriveBase(leftwheel, rightwheel, 62.4, 80)
left_motor = Motor(Port.A, Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.E, Direction.COUNTERCLOCKWISE)
right_motor_2 = Motor(Port.B, Direction.COUNTERCLOCKWISE)
right_motor_3 = Motor(Port.F, Direction.COUNTERCLOCKWISE)

# Initialize variables.
moved_amount = 0

async def move(amount1, speed_1):
    global moved_amount
    await wait(0)
    moved_amount = moved_amount + amount1
    await multitask(
        right_motor.run_angle(speed_1, amount1),
        left_motor.run_angle(speed_1, amount1),
    )

async def Reset(speed_2):
    global moved_amount
    await wait(0)
    if 0 < moved_amount:
        moved_amount = moved_amount + 100
    else:
        if 0 > moved_amount:
            moved_amount = moved_amount - 100
        else:
            moved_amount = 0
    await multitask(
        right_motor.run_angle(speed_2, 0 - moved_amount),
        left_motor.run_angle(speed_2, 0 - moved_amount),
    )
    moved_amount = 0

async def main():
    drive_base.use_gyro(True)
    drive_base.settings(straight_speed=1000)
    drive_base.settings(straight_acceleration=150)
    drive_base.settings(turn_rate=25)
    drive_base.settings(turn_acceleration=100)
    # move (amount in degrees) (speed)
    # await move(3500, 500)
    # Reset (speed)
    # await Reset(500)
    while True:
    # Check if a key has been pressed.
        if keyboard.poll(0):

        # Read the key and print it.
            key = stdin.read(1)
            print("You pressed:", key)


run_task(main())