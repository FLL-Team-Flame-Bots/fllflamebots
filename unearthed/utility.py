from pybricks.hubs import PrimeHub
from pybricks.parameters import Color, Stop
from pybricks.pupdevices import ColorSensor, Motor
from pybricks.robotics import DriveBase
from pybricks.tools import multitask, wait

heading_pid_settings = (7558, 0, 1889, 6, 11)


async def timeout(duration_ms: int, message: str):
    """
    Waits for a specified duration in milliseconds and then prints a message.
    Often used in multitask with race=True to implement timeouts if main task
    gets stuck and does not finish in time.

    Args:
        duration_ms (int): The duration to wait in milliseconds.
        message (str): The message to print after waiting
    """
    await wait(duration_ms)
    print(message)


async def straight_at_speed(
    drive_base: DriveBase, distance: int, speed=-1, acceleration=-1, then=Stop.HOLD
):
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
    if speed != -1:
        drive_base.settings(straight_speed=speed)
    if acceleration != -1:
        drive_base.settings(straight_acceleration=acceleration)
    await drive_base.straight(distance, then=then)
    drive_base.settings(*current_settings)


async def disable_pid(drive_base: DriveBase):
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
        heading_pid_settings[0] / 10,
        0,
        0,
        heading_pid_settings[3],
        heading_pid_settings[4],
    )
    print(f"new heading_pid_settings={drive_base.heading_control().pid()}")


async def enable_pid(drive_base: DriveBase):
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


async def _turn_by_wheel_at_speed(
    prime_hub: PrimeHub,
    drive_base: DriveBase,
    left_wheel: Motor,
    right_wheel: Motor,
    target_angle,
    wheel_speed,
    angle_error,
):
    delta_heading = target_angle - prime_hub.imu.heading()
    while not -angle_error <= delta_heading <= angle_error:
        # negative delta_heading means counter-clockwise turn
        speed = wheel_speed if delta_heading > 0 else -wheel_speed
        left_wheel.run(speed)
        right_wheel.run(-speed)
        await wait(10)
        delta_heading = target_angle - prime_hub.imu.heading()


def normalize_angle(angle):
    """Normalizes an angle to the range [-180, 180).

    Args:
        angle (int): The angle to normalize.

    Returns:
        int: The normalized angle.
    """
    return (angle + 180) % 360 - 180


async def turn_by_wheel(
    prime_hub: PrimeHub,
    drive_base: DriveBase,
    left_wheel: Motor,
    right_wheel: Motor,
    target_angle: int,
    max_turn_speed=200,
    min_turn_speed=30,
):
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
    # Normalize target angle to be within +/- 180 degrees of current heading.
    # prime_hub.imu.heading() can be any value, not limited to [0, 360)
    heading = prime_hub.imu.heading()
    normalized_target = normalize_angle(target_angle - heading) + heading
    # Turn fast until close to target angle
    await _turn_by_wheel_at_speed(
        prime_hub,
        drive_base,
        left_wheel,
        right_wheel,
        normalized_target,
        max_turn_speed,
        10,
    )
    # Turn slow to fine tune the heading
    await _turn_by_wheel_at_speed(
        prime_hub,
        drive_base,
        left_wheel,
        right_wheel,
        normalized_target,
        min_turn_speed,
        1,
    )
    left_wheel.stop()
    right_wheel.stop()
    print(f"heading after TurnByWheel {prime_hub.imu.heading()}")


async def steer_turn(
    prime_hub: PrimeHub,
    left_wheel: Motor,
    right_wheel: Motor,
    target_angle: int,
    max_wheel_speed=200,
    forward=True,
    angle_error=1,
):
    """
    In contrast to DriveBase.turn, this method moves both wheel at same direction (both forward or backward)
    at different speed. It is to avoid the gear backlash when both wheels move in opposite direction.

    Args:
        prime_hub (PrimeHub): The PrimeHub object.
        left_wheel (Motor): The left motor of the robot.
        right_wheel (Motor): The right motor of the robot.
        target_angle (int): The target angle to turn to.
        max_wheel_speed (int, optional): The maximum speed for the faster wheel.
            Defaults to 200.
        forward (bool, optional): Whether the robot should move forward while turning.
            If False, the robot moves backward. Defaults to True.
        angle_error (int, optional): The acceptable error range for the target angle.
            The turn stops when the robot's heading is within this range of the
            target angle. Defaults to 1.

    Returns:
        None
    """
    speed_factor = 1 if forward else -1
    low_wheel_speed = 5 * speed_factor
    heading = prime_hub.imu.heading()
    normalized_target = normalize_angle(target_angle - heading) + heading
    delta_heading = normalized_target - heading

    while not -angle_error <= delta_heading <= angle_error:
        # When orientation is close to target angle, reduce speed to avoid overshoot
        high_wheel_speed = (
            max_wheel_speed if abs(delta_heading) > 5 else 20
        ) * speed_factor
        if (forward and delta_heading > 0) or (not forward and delta_heading < 0):
            left_wheel.run(high_wheel_speed)
            right_wheel.run(low_wheel_speed)
        else:
            right_wheel.run(high_wheel_speed)
            left_wheel.run(low_wheel_speed)
        await wait(10)
        delta_heading = normalized_target - prime_hub.imu.heading()
    left_wheel.hold()
    right_wheel.hold()
    print(f"heading after steer turn {prime_hub.imu.heading()}")


async def move_until_black(
    wheel: Motor, color_sensor: ColorSensor, black_threshold=20, speed=100
):
    wheel.run(speed)
    reflection = await color_sensor.reflection()
    while reflection > black_threshold:
        await wait(10)
        reflection = await color_sensor.reflection()
    wheel.hold()


async def move_until_white(
    wheel: Motor, color_sensor: ColorSensor, white_threshold=90, speed=100
):
    wheel.run(speed)
    reflection = await color_sensor.reflection()
    while reflection < white_threshold:
        await wait(10)
        reflection = await color_sensor.reflection()
    wheel.hold()


async def align_on_color_line(
    left_wheel: Motor,
    right_wheel: Motor,
    left_color_sensor: ColorSensor,
    right_color_sensor: ColorSensor,
    speed=100,
    black_threshold=20,
    white_threshold=90,
):
    # Both wheels move forward until sensed black line
    await multitask(
        move_until_black(left_wheel, left_color_sensor, black_threshold, speed),
        move_until_black(right_wheel, right_color_sensor, black_threshold, speed),
    )
    print("Aligned on black line")
    print(f"Left reflection {await left_color_sensor.reflection()}")
    print(f"Right reflection {await right_color_sensor.reflection()}")

    # At this point both color sensors have detected black line. Move backward
    # until both sensors detect white surface. Thus the base lands between white
    # and black lines.
    await multitask(
        move_until_white(left_wheel, left_color_sensor, white_threshold, -speed),
        move_until_white(right_wheel, right_color_sensor, white_threshold, -speed),
    )
    print("Aligned on white line")
    print(f"Left reflection {await left_color_sensor.reflection()}")
    print(f"Right reflection {await right_color_sensor.reflection()}")
