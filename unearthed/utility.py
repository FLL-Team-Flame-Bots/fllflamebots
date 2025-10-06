from pybricks.parameters import Stop

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
    drive_base.turn(angle - prime_hub.imu.heading())

async def CurveAdjustAngle(
    prime_hub, drive_base, target_angle, radius, max_distance):
    is_forward = max_distance > 0
    first_distance = drive_base.distance()
    delta_angle = target_angle - prime_hub.imu.heading()
    print(
        f"CurveAdjustAngle: start heading={prime_hub.imu.heading()}, " +
        f"start distance={drive_base.distance()}, " +
        f"is_forward={is_forward}"
    )
    while (abs(drive_base.distance() - first_distance) < abs(max_distance)) and (abs(delta_angle) > 2):
        radius = abs(radius) if (is_forward == (delta_angle > 0)) else -abs(radius)
        move_angle = abs(delta_angle) if is_forward else -abs(delta_angle)
        print(
            f"arc(radius={radius}, angle={move_angle})"
        )
        await drive_base.arc(radius, angle=move_angle, then=Stop.COAST_SMART)
        delta_angle = target_angle - prime_hub.imu.heading()
        print(
            f"delta_angle={delta_angle} heading={prime_hub.imu.heading()}"
        )
    print(
        f"final heading={prime_hub.imu.heading()}, " +
        f"distance={drive_base.distance()}"
    )

# The main program starts here.
