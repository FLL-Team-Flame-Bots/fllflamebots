from pybricks.parameters import Stop
from pybricks.tools import multitask, run_task, wait
from unearthed_bot import UnearthedBot
from utility import timeout


bot = UnearthedBot()


async def main():
    await multitask(
        bot.reset_base(),
        bot.reset_right_motor(forward=False),
        bot.reset_left_motor(),
    )
    bot.init_setting()
    drive_base = bot.drive_base
    right_motor = bot.right_motor
    left_motor = bot.left_motor

    # Move forward and turn toward statue mission.
    await drive_base.straight(730)
    await multitask(
        bot.steer_turn(45, max_wheel_speed=300, angle_error=1),
        right_motor.run_target(500, 210),
    )
    print(f"heading after turn to statue {bot.heading()}")

    # Lift statue
    await drive_base.straight(240)
    await multitask(
        right_motor.run_target(500, 30),
        timeout(duration_ms=1000, message="Lift statue timeout"),
        race=True,
    )

    # await drive_base.straight(-15)
    # Rotate dump box to dump artifacts in forum.
    async def dump_artifacts():
        # await wait(500)
        # await drive_base.turn(20)
        await bot.steer_turn(55, max_wheel_speed=300, angle_error=1),
        await left_motor.run_target(300, -200)

    # Retry statue lifting as it may not be fully
    # lifted the first time.
    async def lift_status_retry():
        await wait(500)
        await right_motor.run_target(500, 200)
        await right_motor.run_target(500, 70)
        # await right_motor.run_angle(500, -75)

    # Lifting statue and dumping artifacts can be done in parallel.
    await multitask(
        multitask(lift_status_retry(), dump_artifacts()),
        timeout(duration_ms=2000, message="Dump artifacts timeout"),
        race=True,
    )

    # Backoff from forum and move toward left home.
    # await multitask(lift_status_retry(), dump_artifacts())

    # Backoff from forum and move toward left home.
    await multitask(
        drive_base.straight(-150, then=Stop.HOLD),
        left_motor.run_target(300, 0),
        # right_motor.run_target(500, 0),
    )
    # await drive_base.straight(-180)
    drive_base.settings(turn_rate=360)
    drive_base.settings(turn_acceleration=360)
    await drive_base.turn(45 - bot.heading(), then=Stop.NONE)
    drive_base.settings(straight_speed=1000)
    drive_base.settings(straight_acceleration=1000)
    await drive_base.arc(-900, distance=1000)
    bot.stop()


run_task(main())
