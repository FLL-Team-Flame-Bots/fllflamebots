from pybricks.hubs import PrimeHub
from pybricks.parameters import Axis, Direction, Port, Stop
from pybricks.pupdevices import Motor
from pybricks.robotics import DriveBase
from pybricks.tools import StopWatch, multitask, wait
from utility import normalize_angle, steer_turn, straight_at_speed, turn_by_wheel


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

    async def __reset_motor(self, motor: Motor, forward: bool, speed: int):
        factor = 1 if forward else -1
        await motor.run_until_stalled(factor * speed, Stop.HOLD, 50)
        motor.reset_angle(0)

    async def reset_left_motor(self, forward=True, speed=500):
        await self.__reset_motor(self.left_motor, forward, speed)

    async def reset_right_motor(self, forward=True, speed=500):
        await self.__reset_motor(self.right_motor, forward, speed)

    async def reset_base(self, distance=-10):
        await self.drive_base.straight(distance)
        self.drive_base.reset(0, 0)
        self.drive_base.use_gyro(True)

    def init_setting(self):
        self.watch.reset()
        print("Battery", self.prime_hub.battery.voltage(), sep=", ")
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
        target_angle: int,
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
        distance: int,
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
        Wrapper for the utility function of the same name.
        """
        await steer_turn(
            self.prime_hub,
            self.leftwheel,
            self.rightwheel,
            target_angle,
            max_wheel_speed,
            forward,
            angle_error,
        )
