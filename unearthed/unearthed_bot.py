from pybricks.hubs import PrimeHub
from pybricks.parameters import Axis, Direction, Port, Stop
from pybricks.pupdevices import Motor
from pybricks.robotics import DriveBase
from pybricks.tools import StopWatch, multitask, wait
from utility import straight_at_speed, turn_by_wheel


class UnearthedBot:
    def __init__(self):
        # Set up all devices.
        self.prime_hub = PrimeHub(top_side=Axis.Z, front_side=Axis.X)
        self.watch = StopWatch()
        self.rightwheel = Motor(Port.C, Direction.CLOCKWISE)
        self.leftwheel = Motor(Port.D, Direction.COUNTERCLOCKWISE)
        self.drive_base = DriveBase(self.leftwheel, self.rightwheel, 62.4, 80)
        self.left_motor = Motor(Port.B, Direction.CLOCKWISE)
        self.right_motor = Motor(Port.F, Direction.COUNTERCLOCKWISE)

    async def reset_motor(self, motor: Motor, forward, speed):
        await motor.run_until_stalled(forward * speed, Stop.HOLD, 50)
        motor.reset_angle(0)

    async def reset_left_motor(self, forward=1, speed=500):
        await self.reset_motor(self.left_motor, forward, speed)

    async def reset_right_motor(self, forward=1, speed=500):
        await self.reset_motor(self.right_motor, forward, speed)

    async def reset_base(self, distance=-10):
        await self.drive_base.straight(distance)
        self.drive_base.reset(0, 0)
        self.drive_base.use_gyro(True)

    async def initialize(self):
        self.watch.reset()
        print("Battery", self.prime_hub.battery.voltage(), sep=", ")
        await multitask(
            self.reset_left_motor(),
            self.reset_right_motor(),
            self.reset_base(),
        )
        self.drive_base.settings(straight_speed=600)
        self.drive_base.settings(straight_acceleration=300)
        self.drive_base.settings(turn_rate=100)

    def stop(self):
        self.drive_base.stop()
        print("Stopped, time (ms):", self.watch.time())

    def heading(self) -> float:
        return self.prime_hub.imu.heading()

    async def turn_by_wheel(
        self,
        target_angle: float,
    ):
        await turn_by_wheel(
            self.prime_hub,
            self.drive_base,
            self.leftwheel,
            self.rightwheel,
            target_angle,
        )

    async def straight_at_speed(
        self,
        distance: float,
        speed: int = -1,
        acceleration: int = -1,
        then=Stop.COAST,
    ):
        """
        Wrapper for the utility function of the same name.
        Moves the robot straight for a given distance at a specified speed.
        """
        await straight_at_speed(
            self.drive_base,
            distance,
            speed=speed,
            acceleration=acceleration,
            then=then,
        )

    async def steer_turn(
        self, target_angle: int, max_wheel_speed=200, forward=True, angle_error=1
    ):
        """
        In contrast to DriveBase.turn, this method moves both wheel at same direction (both forward or backward)
        at different speed. It is to avoid the gear backlash when both wheels move in opposite direction.
        """
        speed_factor = 1 if forward else -1
        low_wheel_speed = 5 * speed_factor
        heading = self.heading()
        delta_heading = target_angle - heading
        print(f"steer_turn init heading={heading}")
        print(f"steer_turn init delta angle={delta_heading}")

        while not -angle_error <= delta_heading <= angle_error:
            high_wheel_speed = (
                max_wheel_speed if abs(delta_heading) > 10 else 15
            ) * speed_factor
            if (forward and delta_heading > 0) or (not forward and delta_heading < 0):
                self.leftwheel.run(high_wheel_speed)
                self.rightwheel.run(low_wheel_speed)
            else:
                self.rightwheel.run(high_wheel_speed)
                self.leftwheel.run(low_wheel_speed)
            await wait(10)
            delta_heading = target_angle - self.heading()
        self.leftwheel.stop
        self.rightwheel.stop
        print(f"heading after steer turn {self.heading()}")
