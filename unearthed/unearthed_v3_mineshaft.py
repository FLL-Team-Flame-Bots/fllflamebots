from pybricks.parameters import Stop
from pybricks.tools import multitask, run_task, wait
from unearthed_bot import UnearthedBot
from utility import timeout

bot = UnearthedBot()

# Range:
# Right motor range (-480, 0)
# Left motor range (-296, 0)


async def main():
    # Set up all devices.
    await multitask(
        bot.reset_left_motor(duty_limit=50),
        bot.reset_right_motor(),
        bot.reset_base(),
    )
    bot.init_setting()
    drive_base = bot.drive_base
    left_motor = bot.left_motor
    right_motor = bot.right_motor

    await drive_base.straight(700)
    # await drive_base.turn(90)
    await bot.steer_turn(target_angle=90, max_wheel_speed=300)
    await bot.straight_at_speed(120, speed=300, acceleration=200)

    async def move_after_release_flag():
        await wait(1000)
        await bot.straight_at_speed(240, speed=300, acceleration=300)

    # drop flag
    await multitask(
        right_motor.run_angle(300, -250),
        move_after_release_flag(),
    )

    # Face mission 4, back up a bit, drop right arm all the way down.
    await bot.steer_turn(target_angle=0, forward=False)
    await drive_base.straight(-50)
    await multitask(
        right_motor.run_until_stalled(-300, Stop.HOLD, 50), bot.compensate_backlash()
    )
    print(f"heading after backoff {bot.heading()}")
    print(f"right motor angle after stalled {right_motor.angle()}")
    drive_base.turn(0 - bot.heading())
    # Move toward mission 4, raise right arm to lift mineshaft, then
    # move and continue lifting mineshaft.
    await bot.straight_at_speed(50, speed=300, acceleration=200)
    # await bot.turn_by_wheel(0)  # fine tune as move back&forth would veer off
    print(f"heading toward mission 4 {bot.heading()}")

    await right_motor.run_target(150, -320)

    print(f"right motor angle after lifting shaft {right_motor.angle()}")

    async def lift_shaft_during_move():
        await wait(500)
        await right_motor.run_target(50, -300)

    # Go straight toward mission 4, meanwhile right arm lifting shaft.
    await wait(100)
    await multitask(
        multitask(
            bot.straight_at_speed(150, speed=300, acceleration=200),
            timeout(2000, "straight to mineshaft timeout"),
            race=True,
        ),
        lift_shaft_during_move(),
    )
    print(f"right motor angle after lifting shaft {right_motor.angle()}")
    print(f"heading after lifting shaft {bot.heading()}")

    # Lower left arm to pick up artifact.
    await multitask(
        timeout(2000, "pick up artifact timeout"),
        left_motor.run_until_stalled(-500, Stop.HOLD, 60),
        race=True,
    )
    await left_motor.run_target(150, -20)
    # Back off, turn -180 toward forum
    await drive_base.straight(-120)
    await multitask(
        drive_base.turn(-190),
        right_motor.run_until_stalled(400, Stop.HOLD, 50),
    )
    # Drop the artifact in the forum
    # await left_motor.run_until_stalled(-1000, Stop.HOLD, 50)
    await left_motor.run_target(500, -200, then=Stop.NONE)
    await wait(100)
    await left_motor.run_target(500, 10)
    await bot.steer_turn(80, forward=False, max_wheel_speed=300)
    print(f"heading toward last flag {bot.heading()}")
    await bot.straight_at_speed(
        distance=600, speed=600, acceleration=600, then=Stop.HOLD
    )
    # # await drive_base.straight(530)
    # print(f"heading delivered last flag {bot.heading()}")
    bot.stop()


run_task(main())
