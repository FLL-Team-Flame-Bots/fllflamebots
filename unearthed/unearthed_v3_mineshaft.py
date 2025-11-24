from pybricks.parameters import Stop
from pybricks.pupdevices import Motor
from pybricks.tools import multitask, run_task, wait
from unearthed_bot import UnearthedBot

bot = UnearthedBot()


async def main():
    # Set up all devices.
    await bot.initialize()    
    drive_base = bot.drive_base
    left_motor = bot.left_motor
    right_motor = bot.right_motor

    await drive_base.straight(680)
    #await bot.turn_by_wheel(90)
    await bot.steer_turn(90, max_wheel_speed=300)
    await bot.straight_at_speed(125, speed=300, acceleration=200)
    # drop flag
    await right_motor.run_angle(300, -250)
    await bot.straight_at_speed(240, speed=300, acceleration=150)

    # Face mission 4, back up a bit, drop right arm all the way down.
    await bot.steer_turn(0, forward=False)
    await drive_base.straight(-100)
    await right_motor.run_until_stalled(-300, Stop.HOLD, 50)
    print(f"heading after backoff {bot.heading()}")
    print(f"right motor angle after stalled {right_motor.angle()}")
    # Move toward mission 4, raise right arm to lift mineshaft, then
    # move and continue lifting mineshaft.
    await drive_base.straight(70)
    # await bot.turn_by_wheel(0)  # fine tune as move back&forth would veer off
    print(f"heading toward mission 4 {bot.heading()}")
    await right_motor.run_target(300, -320)
    await wait(500)
    await bot.straight_at_speed(110, speed=200, acceleration=200),
    # await multitask(
    #     bot.straight_at_speed(115, speed=100, acceleration=100),
    #     right_motor.run_target(100, -320),
    # )
    print(f"right motor angle after lifting shaft {right_motor.angle()}")
    print(f"heading after lifting shaft {bot.heading()}")
    await bot.turn_by_wheel(0)

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
        right_motor.run_until_stalled(400, Stop.HOLD, 50)
    )
    # Drop the artifact in the forum
    await left_motor.run_target(-1000, -150)
    await left_motor.run_until_stalled(1000, Stop.HOLD, 50)    
    await drive_base.straight(-70)
    await bot.turn_by_wheel(70)
    print(f"heading toward last flag {bot.heading()}")
    await drive_base.straight(460)
    print(f"heading delivered last flag {bot.heading()}")
    bot.stop()


run_task(main())
