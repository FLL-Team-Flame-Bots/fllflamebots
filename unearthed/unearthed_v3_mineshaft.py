from pybricks.parameters import Stop
from pybricks.pupdevices import Motor
from pybricks.tools import multitask, run_task, wait
from unearthed_bot import UnearthedBot

bot = UnearthedBot()


async def main():
    # Set up all devices.
    bot.initialize()
    prime_hub = bot.prime_hub
    drive_base = bot.drive_base
    left_motor = bot.left_motor
    right_motor = bot.right_motor

    await drive_base.straight(710)
    await bot.turn_by_wheel(90)
    await bot.straight_at_speed(110, speed=300, acceleration=200)
    # drop flag
    await right_motor.run_angle(300, -200)
    await bot.straight_at_speed(185, speed=300, acceleration=200)

    # Face mission 4, back up a bit, drop right arm all the way down.
    await bot.turn_by_wheel(0)
    await drive_base.straight(-135)
    await right_motor.run_until_stalled(-300, Stop.HOLD, 50)
    print(f"heading after backoff {bot.heading()}")
    print(f"right motor angle after stalled {right_motor.angle()}")
    # Move toward mission 4, raise right arm to lift mineshaft, then
    # move and continue lifting mineshaft.
    await drive_base.straight(80)
    await bot.turn_by_wheel(0)  # fine tune as move back&forth would veer off
    print(f"heading toward mission 4 {bot.heading()}")
    await right_motor.run_target(300, -370)
    await multitask(
        bot.straight_at_speed(115, speed=140, acceleration=100),
        right_motor.run_target(200, -320),
    )
    await bot.turn_by_wheel(0)
    # await wait(100)

    # Lower left arm to pick up artifact.
    await multitask(
        wait(2000),
        left_motor.run_until_stalled(-500, Stop.HOLD, 80),
        race=True,
    )
    await left_motor.run_angle(150, 270)
    # Back off, turn -180 toward forum
    await multitask(
        drive_base.straight(-90), right_motor.run_until_stalled(400, Stop.HOLD, 50)
    )
    await drive_base.turn(-180)
    await left_motor.run_target(-1000, -150)
    await left_motor.run_until_stalled(1000, Stop.HOLD, 50)
    # await left_motor.run_angle(1000, 100)
    await drive_base.straight(-70)
    await bot.turn_by_wheel(70)
    print(f"heading toward last flag {bot.heading()}")
    await drive_base.straight(460)
    print(f"heading delivered last flag {bot.heading()}")
    bot.stop()


run_task(main())
