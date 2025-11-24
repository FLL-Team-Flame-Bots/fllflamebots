from pybricks.hubs import PrimeHub
from pybricks.parameters import Axis, Direction, Port, Stop
from pybricks.pupdevices import Motor
from pybricks.robotics import DriveBase
from pybricks.tools import multitask, run_task, wait

from unearthed_bot import UnearthedBot

# Set up all devices.
bot = UnearthedBot()


async def main():
    print("Battery", bot.prime_hub.battery.voltage(), sep=", ")
    drive_base = bot.drive_base
    await drive_base.straight(-200)
    print("Heading after straight:", bot.heading())
    await bot.steer_turn(90, forward=True)
    print("Heading after 90 steer turn:", bot.heading())
    await drive_base.straight(100)
    print("Heading after 2nd straight:", bot.heading())

    # await drive_base.straight(-10)
    # await drive_base.straight(750, Stop.COAST)
    # await turn_by_wheel(prime_hub, drive_base, leftwheel, rightwheel, 90)
    # disable_pid(drive_base)
    # await drive_base.straight(150)
    # print(f"heading after straight {prime_hub.imu.heading()} drive_base angle {drive_base.angle()}")
    # enable_pid(drive_base)


run_task(main())
