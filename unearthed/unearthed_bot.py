from pybricks.hubs import PrimeHub
from pybricks.parameters import Axis, Direction, Port, Stop
from pybricks.pupdevices import Motor
from pybricks.robotics import DriveBase
from pybricks.tools import StopWatch
from utility import (
    steer_turn,
    straight_at_speed,
    turn_at_rate,
    turn_by_wheel,
    turn_to_target,
    compensate_backlash,
)


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

    async def __reset_motor(
        self, motor: Motor, forward: bool, speed: int, duty_limit: int = 50
    ):
        factor = 1 if forward else -1
        await motor.run_until_stalled(factor * speed, Stop.HOLD, duty_limit)
        motor.reset_angle(0)

    async def reset_left_motor(self, forward=True, speed=500, duty_limit=50):
        await self.__reset_motor(self.left_motor, forward, speed, duty_limit)

    async def reset_right_motor(self, forward=True, speed=500, duty_limit=50):
        await self.__reset_motor(self.right_motor, forward, speed, duty_limit)

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
        return self.drive_base.angle()

    async def turn_to_target(self, target_angle: int):
        await turn_to_target(self.drive_base, target_angle)

    async def turn_by_wheel(
        self,
        target_angle: int,
    ):
        await turn_by_wheel(
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

    async def turn_at_rate(
        self,
        angle: int,
        turn_rate: int = -1,
        turn_acceleration: int = -1,
        then=Stop.COAST,
    ):
        """
        Wrapper for the utility function of the same name.
        Turns the robot for a given angle at a specified rate.
        """
        await turn_at_rate(
            self.drive_base,
            angle,
            turn_rate=turn_rate,
            turn_acceleration=turn_acceleration,
            then=then,
        )

    async def steer_turn(
        self, target_angle: int, forward=True, max_wheel_speed=200, angle_error=1
    ):
        """
        Wrapper for the utility function of the same name.
        """
        await steer_turn(
            self.drive_base,
            self.leftwheel,
            self.rightwheel,
            target_angle,
            forward,
            max_wheel_speed,
            angle_error,
        )

    async def compensate_backlash(self, forward=True):
        compensate_backlash(self.leftwheel, self.rightwheel, forward)

    async def adjust_target_angle(self, target_angle: int):
        turn_to_target(self.drive_base, target_angle)

    def voltage(self) -> int:
        return self.prime_hub.battery.voltage()
