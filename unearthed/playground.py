from pybricks.parameters import Stop
from pybricks.pupdevices import Motor
from pybricks.tools import multitask, run_task, wait
from unearthed_bot import UnearthedBot
from utility import timeout

bot = UnearthedBot()


async def main():
    right_motor = bot.right_motor
    # await bot.reset_right_motor()
    await right_motor.run_until_stalled(-300, Stop.HOLD, 50)
    # await bot.drive_base.straight(100)
    # await right_motor.run_target(speed=150, target_angle=-300)
    await right_motor.run_angle(speed=150, rotation_angle=170)


run_task(main())
