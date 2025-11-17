from pybricks.hubs import PrimeHub
from pybricks.parameters import Color, Stop
from pybricks.pupdevices import ColorSensor, Motor
from pybricks.robotics import DriveBase
from pybricks.tools import multitask, wait

heading_pid_settings = ()

async def StraightAtSpeed(drive_base : DriveBase,
                          distance : int,
                          speed = -1,
                          acceleration = -1,
                          then=Stop.HOLD):
    """
    Moves the robot straight for a given distance at a specified speed and acceleration.
    Afterwards, set speed and acceleration back to their original values.

    Args:
        drive_base (DriveBase): The drive base object.
        distance (int): The distance to move in millimeters.
        speed (int, optional): The straight speed. Defaults to -1 (uses current setting).
        acceleration (int, optional): The straight acceleration. Defaults to -1 (uses current setting).
        then (Stop, optional): The stop behavior after moving. Defaults to Stop.HOLD.
    """
    current_settings = drive_base.settings()
    if speed != -1: drive_base.settings(straight_speed=speed)
    if acceleration != -1: drive_base.settings(straight_acceleration=acceleration)
    await drive_base.straight(distance, then=then)
    drive_base.settings(*current_settings)


async def DisablePID(drive_base : DriveBase):
    """Disables the PID control for the robot's heading.

    This function saves the current heading PID settings to a global
    variable, and then sets the integral and derivative gains to 0,
    effectively disabling the PID control. The proportional gain is
    reduced to 1/10th of its original value.

    Args:
        drive_base: The DriveBase object for the robot.
    """
    global heading_pid_settings
    heading_pid_settings = drive_base.heading_control().pid()
    print(f"previous heading_pid_settings={heading_pid_settings}")
    drive_base.heading_control.pid(
        heading_pid_settings[0]/10, 0, 0, heading_pid_settings[3], heading_pid_settings[4])
    print(f"new heading_pid_settings={drive_base.heading_control().pid()}")

async def EnablePID(drive_base : DriveBase):
    """Restores the heading PID control to its original settings.

    This function restores the PID gains (proportional, integral, derivative)
    that were saved by a prior call to DisablePID(). It uses the values
    stored in the global `heading_pid_settings` variable.

    This should be called after a maneuver that required PID to be disabled.

    Args:
        drive_base (DriveBase): The drive base object.
    """
    global heading_pid_settings    
    if not heading_pid_settings:
        print("heading_pid_settings is empty, cannot enable PID.")
        return
    
    print(f"previous heading_pid_settings={drive_base.heading_control().pid()}")
    drive_base.heading_control.pid(*heading_pid_settings)
    print(f"new heading_pid_settings={drive_base.heading_control().pid()}")


async def _TurnByWheelAtSpeed(prime_hub : PrimeHub,
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
        speed = wheel_speed if delta_heading > 0 else -wheel_speed
        left_wheel.run(speed)
        right_wheel.run(-speed)
        await wait(10)        
        delta_heading = target_angle - prime_hub.imu.heading()
    print(f"heading after turn {angle_error} {prime_hub.imu.heading()}")

async def TurnByWheel(prime_hub : PrimeHub,
                      drive_base : DriveBase,
                      left_wheel : Motor, 
                      right_wheel : Motor, 
                      target_angle : int):
    """Turns the robot to a specific angle.

    This function turns the robot to a given target angle by first turning
    at a high speed to get close to the target, and then slowing down to
    fine-tune the heading.

    Args:
        prime_hub: The PrimeHub object.
        drive_base: The DriveBase object for the robot.
        left_wheel: The left motor of the robot.
        right_wheel: The right motor of the robot.
        target_angle: The target angle to turn to.
    """
    print(f"TurnByWheel target_angle={target_angle}")
    # Turn fast until close to target angle
    await _TurnByWheelAtSpeed(prime_hub, drive_base, left_wheel, right_wheel, target_angle, 200, 10)
    # Turn slow to fine tune the heading
    await _TurnByWheelAtSpeed(prime_hub, drive_base, left_wheel, right_wheel, target_angle, 30, 1)
    left_wheel.stop()
    right_wheel.stop()
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
