from pybricks.parameters import Color, Stop
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
