from pybricks.parameters import Stop

async def AccurateTurn(prime_hub, drive_base, angle):
    print(['accurate turn angle', angle])
    repeated = 0
    delta_heading = 0
    repeated = 0
    delta_heading = angle - prime_hub.imu.heading()
    print(['init delta angle', delta_heading])
    await drive_base.turn(1 * delta_heading, then=Stop.COAST)
    delta_heading = angle - prime_hub.imu.heading()
    print(['2nd delta angle', delta_heading])
    while not -2 <= delta_heading <= 2:      
        repeated += 1
        await drive_base.turn(1.2 * delta_heading, then=Stop.COAST)
        delta_heading = angle - prime_hub.imu.heading()
        print(['repeat delta angle', delta_heading, repeated])
        if repeated > 3:
            break
    drive_base.stop()


# The main program starts here.
