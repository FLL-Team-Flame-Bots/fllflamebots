from pybricks.parameters import Stop

async def AccurateTurn(prime_hub, drive_base, angle):
    repeated = 0
    delta_heading = 0
    repeated = 0
    delta_heading = angle - prime_hub.imu.heading()
    await drive_base.turn(1 * delta_heading, then=Stop.COAST)
    delta_heading = angle - prime_hub.imu.heading()
    while not -2 <= delta_heading <= 2:
        repeated += 1
        await drive_base.turn(1.5 * delta_heading, then=Stop.COAST)
        delta_heading = angle - prime_hub.imu.heading()
        if repeated > 3:
            break
    drive_base.stop()


# The main program starts here.
