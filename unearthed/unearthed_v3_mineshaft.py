from pybricks.parameters import Stop
from pybricks.pupdevices import Motor
from pybricks.tools import multitask, run_task, wait
from unearthed_bot import UnearthedBot
from utility import timeout

bot = UnearthedBot()


async def main():
    # Set up all devices.
    await multitask(
        bot.reset_left_motor(),
        bot.reset_right_motor(),
        bot.reset_base(),
    )
    bot.init_setting()
    drive_base = bot.drive_base
    left_motor = bot.left_motor
    right_motor = bot.right_motor

    await drive_base.straight(680)
    # await bot.turn_by_wheel(90)
    await bot.steer_turn(90, max_wheel_speed=300)
    await bot.straight_at_speed(80, speed=300, acceleration=200)
    # drop flag
    await multitask(
        right_motor.run_angle(300, -250),
        bot.straight_at_speed(260, speed=300, acceleration=150),
    )

    # Face mission 4, back up a bit, drop right arm all the way down.
    await bot.steer_turn(0, forward=False)
    await drive_base.straight(-100)
    await right_motor.run_until_stalled(-300, Stop.HOLD, 50)
    print(f"heading after backoff {bot.heading()}")
    print(f"right motor angle after stalled {right_motor.angle()}")
    # Move toward mission 4, raise right arm to lift mineshaft, then
    # move and continue lifting mineshaft.
    await bot.straight_at_speed(85, speed=200, acceleration=100)
    # await bot.turn_by_wheel(0)  # fine tune as move back&forth would veer off
    print(f"heading toward mission 4 {bot.heading()}")

    async def lift_shaft_stuck():
        await wait(1000)
        print("Lifting shaft stuck")
        await drive_base.straight(-10)

    await multitask(
        right_motor.run_target(200, -320),
        lift_shaft_stuck(),
        race=True,
    )
    await right_motor.run_target(200, -320)

    print(f"right motor angle after lifting shaft {right_motor.angle()}")

    async def lift_shaft_during_move():
        await wait(500)
        await right_motor.run_target(100, -310)

    await wait(500)
    await multitask(
        multitask(
            bot.straight_at_speed(130, speed=300, acceleration=200),
            timeout(2000, "straight to mineshaft timeout"),
            race=True,
        ),
        lift_shaft_during_move(),
    )
    print(f"right motor angle after lifting shaft {right_motor.angle()}")
    print(f"heading after lifting shaft {bot.heading()}")

    # Lower left arm to pick up artifact.
    await multitask(
        wait(2000),
        left_motor.run_until_stalled(-500, Stop.HOLD, 80),
        race=True,
    )
    await left_motor.run_angle(150, 270)
    # Back off, turn -180 toward forum
    await drive_base.straight(-70)
    await multitask(
        drive_base.turn(-180),
        right_motor.run_until_stalled(400, Stop.HOLD, 50),
    )
    # Drop the artifact in the forum
    await left_motor.run_target(-1000, -150)
    await left_motor.run_until_stalled(1000, Stop.HOLD, 50)
    await bot.steer_turn(68, forward=False, max_wheel_speed=300)
    print(f"heading toward last flag {bot.heading()}")
    await drive_base.straight(530)
    print(f"heading delivered last flag {bot.heading()}")
    bot.stop()


run_task(main())
