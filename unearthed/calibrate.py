from pybricks.parameters import Stop
from pybricks.pupdevices import Motor
from pybricks.tools import multitask, run_task, wait
from unearthed_bot import UnearthedBot
from utility import timeout

bot = UnearthedBot()


async def main():
    await bot.reset_right_motor()
    await bot.right_motor.run_until_stalled(-300, Stop.HOLD, 50)
    print(f"Right motor range ({bot.right_motor.angle()}, 0)")

    await bot.reset_left_motor()
    await bot.left_motor.run_until_stalled(-300, Stop.HOLD, 50)
    print(f"Left motor range ({bot.left_motor.angle()}, 0)")


run_task(main())
