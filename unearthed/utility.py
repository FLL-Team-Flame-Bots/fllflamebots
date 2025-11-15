from pybricks.hubs import PrimeHub
from pybricks.parameters import Color, Stop
from pybricks.pupdevices import ColorSensor, Motor
from pybricks.robotics import DriveBase
from pybricks.tools import multitask, wait

heading_pid_settings = ()


async def AccurateTurn(prime_hub, drive_base, angle, adjust_factor=1):
    print(f"AccurateTurn angle={angle}")
    repeated = 0
    delta_heading = 0
    repeated = 0
    delta_heading = angle - prime_hub.imu.heading()
    print(f"init heading={prime_hub.imu.heading()}")
    print(f"init delta angle={delta_heading}")
    drive_base.turn(1 * delta_heading, then=Stop.HOLD)
    delta_heading = angle - prime_hub.imu.heading()
    while not -2 <= delta_heading <= 2:
        repeated += 1
        print(f"repeated={repeated} heading={prime_hub.imu.heading()}")
        await drive_base.turn(adjust_factor * delta_heading, then=Stop.HOLD)
        delta_heading = angle - prime_hub.imu.heading()
        if repeated > 3:
            break
    drive_base.stop()


async def StraightAtSpeed(drive_base : DriveBase,
                          distance : int,
                          speed = -1,
                          acceleration = -1,
                          then=Stop.HOLD):
    current_settings = drive_base.settings()
    if speed != -1: drive_base.settings(straight=speed)
    if acceleration != -1: drive_base.settings(straight_acceleration=acceleration)
    await drive_base.straight(distance, then=then)
    drive_base.settings(current_settings)


async def DisablePID(drive_base : DriveBase):
    global heading_pid_settings
    heading_pid_settings = drive_base.heading_control().pid()
    print(f"previous heading_pid_settings={heading_pid_settings}")
    drive_base.heading_control.pid(
        heading_pid_settings[0]/10, 0, 0, heading_pid_settings[3], heading_pid_settings[4])
    print(f"new heading_pid_settings={drive_base.heading_control().pid()}")

async def EnablePID(drive_base : DriveBase):
    print(f"previous heading_pid_settings={drive_base.heading_control().pid()}")
    drive_base.heading_control.pid(
        heading_pid_settings[0], 
        heading_pid_settings[1], 
        heading_pid_settings[2], 
        heading_pid_settings[3], 
        heading_pid_settings[4])
    print(f"new heading_pid_settings={drive_base.heading_control().pid()}")


async def TurnByWheelAtSpeed(prime_hub : PrimeHub,
                             drive_base : DriveBase,
                             left_wheel : Motor,
                             right_wheel : Motor,
                             target_angle, wheel_speed, angle_error):
    delta_heading = target_angle - prime_hub.imu.heading()
    print(f"init heading={prime_hub.imu.heading()}")
    print(f"init drive_base angle={drive_base.angle()}")
    print(f"init delta angle={delta_heading}")
    while not -angle_error <= delta_heading <= angle_error:
        # negative delta_heading means counter-clockwise turn
        if delta_heading < 0: wheel_speed = -wheel_speed
        left_wheel.run(wheel_speed)
        right_wheel.run(-wheel_speed)
        await wait(10)        
        delta_heading = target_angle - prime_hub.imu.heading()
    print(f"heading after turn error {angle_error} {prime_hub.imu.heading()}")

async def TurnByWheel(prime_hub : PrimeHub,
                      drive_base : DriveBase,
                      left_wheel : Motor, 
                      right_wheel : Motor, 
                      target_angle : int):
    drive_base.stop()
    print(f"TurnByWheel target_angle={target_angle}")
    # Turn fast until close to target angle
    await TurnByWheelAtSpeed(prime_hub, drive_base, left_wheel, right_wheel, target_angle, 100, 10)
    # Turn slow to fine tune the heading
    await TurnByWheelAtSpeed(prime_hub, drive_base, left_wheel, right_wheel, target_angle, 30, 1)
    left_wheel.brake()
    right_wheel.brake()
    #await drive_base.turn(target_angle - prime_hub.imu.heading())
    drive_base.reset(0, prime_hub.imu.heading())
    print(f"heading after TurnByWheel {prime_hub.imu.heading()} drive_base angle {drive_base.angle()}")


async def MoveUntilBlack(wheel : Motor,
                         color_sensor : ColorSensor,
                         black_threshold=20,                         
                         speed=100):
    wheel.run(speed)
    reflection = await color_sensor.reflection()
    while reflection > black_threshold:
        await wait(10)
        reflection = await color_sensor.reflection()
    wheel.hold()

async def MoveUntilWhite(wheel : Motor,
                         color_sensor : ColorSensor,
                         white_threshold=90,                         
                         speed=100):
    wheel.run(speed)
    reflection = await color_sensor.reflection()
    while reflection < white_threshold:
        await wait(10)
        reflection = await color_sensor.reflection()
    wheel.hold()

async def AlignOnColorLine(left_wheel : Motor, 
                           right_wheel : Motor, 
                           left_color_sensor : ColorSensor,
                           right_color_sensor : ColorSensor, 
                           speed=100,
                           black_threshold=20,
                           white_threshold=90):    
    # Both wheels move forward until sensed black line
    await multitask(
        MoveUntilBlack(left_wheel, left_color_sensor, black_threshold, speed),
        MoveUntilBlack(right_wheel, right_color_sensor, black_threshold, speed)
    )
    print("Aligned on black line")
    print(f"Left reflection {await left_color_sensor.reflection()}")
    print(f"Right reflection {await right_color_sensor.reflection()}")

    # At this point both color sensors have detected black line. Move backward 
    # until both sensors detect white surface. Thus the base lands between white 
    # and black lines.
    await multitask(
        MoveUntilWhite(left_wheel, left_color_sensor, white_threshold, -speed),
        MoveUntilWhite(right_wheel, right_color_sensor, white_threshold, -speed)
    )
    print("Aligned on white line")
    print(f"Left reflection {await left_color_sensor.reflection()}")
    print(f"Right reflection {await right_color_sensor.reflection()}")
