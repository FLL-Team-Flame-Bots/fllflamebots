from pybricks.parameters import Color, Stop
from pybricks.pupdevices import ColorSensor, Motor
from pybricks.tools import multitask, wait


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


async def TurnByWheel(prime_hub, drive_base, left_wheel, right_wheel, target_angle, wheel_speed=30, angle_error=1):
    drive_base.stop()
    print(f"AccurateTurnWithWheel target_angle={target_angle}")
    repeated = 0
    delta_heading = 0
    repeated = 0
    delta_heading = target_angle - prime_hub.imu.heading()
    print(f"init heading={prime_hub.imu.heading()}")
    print(f"init delta angle={delta_heading}")
    while not -angle_error <= delta_heading <= angle_error:
        if delta_heading > 0: # clockwise turn
            left_wheel.run(wheel_speed)
            right_wheel.run(-wheel_speed)
        else: # counter-clockwise turn
            left_wheel.run(-wheel_speed)
            right_wheel.run(wheel_speed)
        await wait(10)        
        delta_heading = target_angle - prime_hub.imu.heading()        
    left_wheel.stop()
    right_wheel.stop()
    await drive_base.turn(target_angle - prime_hub.imu.heading())    
    print(f"heading after turn {prime_hub.imu.heading()}")

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
