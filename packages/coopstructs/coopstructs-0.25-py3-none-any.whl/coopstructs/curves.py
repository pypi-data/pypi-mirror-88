from enum import Enum
from abc import ABC, abstractmethod
from coopstructs.vectors import Vector2
import math
from typing import List, Callable
from coopstructs.toggles import EnumToggleable
from coopstructs.geometry import Rectangle

class Orientation(Enum):
    UP_LEFT = 3
    UP_RIGHT = 4
    RIGHT_UP = 5
    RIGHT_DOWN = 6
    DOWN_RIGHT = 7
    DOWN_LEFT = 8
    LEFT_DOWN = 9
    LEFT_UP = 10
    UP = 11
    RIGHT = 12
    DOWN = 13
    LEFT = 14


class Curve(ABC):
    def __init__(self, id: str, origin: Vector2):
        self.origin = origin
        self.id = id

    def __str__(self):
        return f"{type(self)} starting at {self.origin} and terminating at {self.end_point()} [{self.id}]"

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return self.__str__()

    @abstractmethod
    def end_point(self):
        pass

    @abstractmethod
    def line_representation(self) -> List:
        pass

    @abstractmethod
    def force_continuity(self, next_point: Vector2) -> Vector2:
        pass

    @classmethod
    def orientation(cls, origin, destination) -> List[Orientation]:
        orientation = None
        if origin.x == destination.x and origin.y > destination.y:
            orientation = [Orientation.UP]
        elif origin.x == destination.x and origin.y < destination.y:
            orientation = [Orientation.DOWN]
        elif origin.x < destination.x and origin.y == destination.y:
            orientation = [Orientation.RIGHT]
        elif origin.x > destination.x and origin.y == destination.y:
            orientation = [Orientation.LEFT]
        elif origin.x > destination.x and origin.y > destination.y:
            orientation = [Orientation.UP_LEFT, Orientation.LEFT_UP]
        elif origin.x > destination.x and origin.y < destination.y:
            orientation = [Orientation.DOWN_LEFT, Orientation.LEFT_DOWN]
        elif origin.x < destination.x and origin.y > destination.y:
            orientation = [Orientation.UP_RIGHT, Orientation.RIGHT_UP]
        elif origin.x < destination.x and origin.y < destination.y:
            orientation = [Orientation.DOWN_RIGHT, Orientation.RIGHT_DOWN]
        return orientation


class Arc(Curve):

    @classmethod
    def from_arcbox(cls, id:str, orientation: Orientation, origin: Vector2, arc_box_size: Vector2):
        return Arc(id, orientation, origin, arc_box_size)

    @classmethod
    def from_origin_and_destination(cls, id:str, orientation: Orientation, origin: Vector2, destination: Vector2):
        return Arc(id, orientation, origin, Vector2(destination.x - origin.x, destination.y - origin.y) * 2)

    def __init__(self, id:str, orientation: Orientation, origin: Vector2, arc_box_size: Vector2):
        super().__init__(id, origin)
        self.orientation = orientation
        self.arc_box_size = arc_box_size
        self.arc_rad_start = None
        self.arc_rad_end = None
        self.define_arc_radian_start_end()
        self._arc_box = self.arc_box()
        self.mid_point = Vector2(self._arc_box[0] + self._arc_box[2] / 2.0, self._arc_box[1] + self._arc_box[3] / 2.0)

    def line_representation(self):
        return self.compute_curve_lines()

    def define_arc_radian_start_end(self):
        if self.orientation == Orientation.DOWN_LEFT:
            self.arc_rad_start = 2 * math.pi
            self.arc_rad_end = 3 * math.pi / 2
        elif self.orientation == Orientation.DOWN_RIGHT:
            self.arc_rad_start = math.pi
            self.arc_rad_end = 3 * math.pi / 2
        elif self.orientation == Orientation.LEFT_DOWN:
            self.arc_rad_start = math.pi / 2
            self.arc_rad_end = math.pi
        elif self.orientation == Orientation.LEFT_UP:
            self.arc_rad_start = 3 * math.pi / 2
            self.arc_rad_end = math.pi
        elif self.orientation == Orientation.UP_LEFT:
            self.arc_rad_start = 0
            self.arc_rad_end = math.pi / 2
        elif self.orientation == Orientation.UP_RIGHT:
            self.arc_rad_start = math.pi
            self.arc_rad_end = math.pi / 2
        elif self.orientation == Orientation.RIGHT_DOWN:
            self.arc_rad_start = math.pi / 2
            self.arc_rad_end = 0
        elif self.orientation == Orientation.RIGHT_UP:
            self.arc_rad_start = 3 * math.pi / 2
            self.arc_rad_end = 2 * math.pi
        else:
            raise Exception(f"Invalid curve orientation: [{self.orientation}]")

    def end_point(self):
        if self.orientation in (Orientation.DOWN_LEFT,  Orientation.LEFT_DOWN):
            return Vector2(int(self.origin.x - self.arc_box_size.x / 2), int(self.origin.y + self.arc_box_size.y / 2))
        elif self.orientation in (Orientation.LEFT_UP, Orientation.UP_LEFT):
            return Vector2(int(self.origin.x - self.arc_box_size.x / 2), int(self.origin.y - self.arc_box_size.y / 2))
        elif self.orientation in (Orientation.UP_RIGHT, Orientation.RIGHT_UP):
            return Vector2(int(self.origin.x + self.arc_box_size.x / 2), int(self.origin.y - self.arc_box_size.y / 2))
        elif self.orientation in (Orientation.RIGHT_DOWN, Orientation.DOWN_RIGHT):
            return Vector2(int(self.origin.x + self.arc_box_size.x / 2), int(self.origin.y + self.arc_box_size.y / 2))
        else:
            raise Exception("Incorrect Curve type with orientation")

    def compute_curve_lines(self):
        b_points = self.compute_curve_points()
        if b_points is None:
            return None

        ret = []
        for ii in range(0, len(b_points)):
            if ii == 0:
                continue
            else:
                start = Vector2(b_points[ii - 1].x, b_points[ii - 1].y)
                end = Vector2(b_points[ii].x, b_points[ii].y)
                ret.append(Line(self.id + f"_{ii}", start, end))
        return ret

    def compute_curve_points(self, numPoints=None) -> List[Vector2]:
        if numPoints is None:
            numPoints = 30
        if numPoints < 2:
            return None

        ret = []
        increment = (self.arc_rad_end - self.arc_rad_start) / (numPoints - 1)
        for ii in range(0, numPoints):
            next = self.point_along_arc(self.arc_rad_start + increment * ii, self.mid_point, self.arc_box_as_rectangle())
            ret.append(next)

        return ret

    def arc_box_as_rectangle(self) -> Rectangle:
        return Rectangle(x=self._arc_box[0], y=self._arc_box[1], width=self._arc_box[2], height=self._arc_box[3])

    def point_along_arc(self, radians: float, rotation_point: Vector2, arc_box: Rectangle):
        a = arc_box.width / 2
        b = arc_box.height / 2

        x = a * math.cos(radians)
        y = - b * math.sin(radians)

        return Vector2(int(x), int(y)) + rotation_point

    def arc_box(self):
        if self.orientation == Orientation.DOWN_LEFT:
            return [self.origin.x - self.arc_box_size.x, self.origin.y - self.arc_box_size.y / 2,
                    self.arc_box_size.x, self.arc_box_size.y]
        elif self.orientation == Orientation.DOWN_RIGHT:
            return [self.origin.x, self.origin.y - self.arc_box_size.y / 2,
                    self.arc_box_size.x, self.arc_box_size.y]
        elif self.orientation == Orientation.LEFT_DOWN:
            return [self.origin.x - self.arc_box_size.x / 2, self.origin.y,
                    self.arc_box_size.x, self.arc_box_size.y]
        elif self.orientation == Orientation.LEFT_UP:
            return [self.origin.x - self.arc_box_size.x / 2, self.origin.y - self.arc_box_size.y,
                    self.arc_box_size.x, self.arc_box_size.y]
        elif self.orientation == Orientation.UP_LEFT:
            return [self.origin.x - self.arc_box_size.x, self.origin.y - self.arc_box_size.y / 2,
                    self.arc_box_size.x, self.arc_box_size.y]
        elif self.orientation == Orientation.UP_RIGHT:
            return [self.origin.x, self.origin.y - self.arc_box_size.y / 2,
                    self.arc_box_size.x, self.arc_box_size.y]
        elif self.orientation == Orientation.RIGHT_UP:
            return [self.origin.x - self.arc_box_size.x / 2, self.origin.y - self.arc_box_size.y,
                    self.arc_box_size.x, self.arc_box_size.y]
        elif self.orientation == Orientation.RIGHT_DOWN:
            return [self.origin.x - self.arc_box_size.x / 2, self.origin.y,
                    self.arc_box_size.x, self.arc_box_size.y]
        else:
            raise Exception("Incorrect Curve type with orientation")

    def length(self):
        return (self.arc_rad_end - self.arc_rad_start) * (self.origin - self.mid_point).length()

    def force_continuity(self, next_point: Vector2) -> Vector2:
        end_point = self.end_point()
        if self.orientation in (Orientation.UP_LEFT, Orientation.DOWN_LEFT) and next_point.x > end_point.x:
            return Vector2(end_point.x, next_point.y)
        elif self.orientation in (Orientation.UP_RIGHT, Orientation.DOWN_RIGHT) and next_point.x < end_point.x:
            return Vector2(end_point.x, next_point.y)
        elif self.orientation in (Orientation.RIGHT_UP, Orientation.LEFT_UP) and next_point.y > end_point.y:
            return Vector2(next_point.x, end_point.y)
        elif self.orientation in (Orientation.RIGHT_DOWN, Orientation.LEFT_DOWN) and next_point.y < end_point.y:
            return Vector2(next_point.x, end_point.y)
        else:
            return next_point



class Line(Curve):
    def __init__(self, id:str, origin: Vector2, destination: Vector2):
        super().__init__(id, origin)
        self.destination = destination
        self.length = self.length()

    def line_representation(self):
        return [self]

    def end_point(self):
        return self.destination

    def length(self):
        try:
            return math.sqrt((self.destination.x - self.origin.x) ** 2 + (self.destination.y - self.origin.y) ** 2)
        except Exception as e:
            print(f"Destination: {self.destination}\n"
                  f"Origin: {self.origin}\n"
                  f"{e}")
            raise

    def force_continuity(self, next_point: Vector2) -> Vector2:
        return next_point

class CubicBezier(Curve):
    def __init__(self, id:str, control_points: List[Vector2]):
        Curve.__init__(self, id, control_points[0])
        self.control_points = control_points

    def line_representation(self):
        return self.compute_curve_lines()

    def end_point(self):
        return self.control_points[-1]

    def compute_curve_lines(self):
        b_points = self.compute_bezier_points([(x.x, x.y) for x in self.control_points])
        ret = []
        for ii in range(0, len(b_points)):
            if ii == 0:
                continue
            else:
                start = Vector2(b_points[ii - 1][0], b_points[ii - 1][1])
                end = Vector2(b_points[ii][0], b_points[ii][1])
                ret.append(Line(self.id + f"_{ii}", start, end))
        return ret

    def compute_bezier_points(self, vertices, numPoints=None):
        if numPoints is None:
            numPoints = 30
        if numPoints < 2 or len(vertices) != 4:
            return []

        result = []

        b0x = vertices[0][0]
        b0y = vertices[0][1]
        b1x = vertices[1][0]
        b1y = vertices[1][1]
        b2x = vertices[2][0]
        b2y = vertices[2][1]
        b3x = vertices[3][0]
        b3y = vertices[3][1]

        # Compute polynomial coefficients from Bezier points
        ax = -b0x + 3 * b1x + -3 * b2x + b3x
        ay = -b0y + 3 * b1y + -3 * b2y + b3y

        bx = 3 * b0x + -6 * b1x + 3 * b2x
        by = 3 * b0y + -6 * b1y + 3 * b2y

        cx = -3 * b0x + 3 * b1x
        cy = -3 * b0y + 3 * b1y

        dx = b0x
        dy = b0y

        # Set up the number of steps and step size
        numSteps = numPoints - 1  # arbitrary choice
        h = 1.0 / numSteps  # compute our step size

        # Compute forward differences from Bezier points and "h"
        pointX = dx
        pointY = dy

        firstFDX = ax * (h * h * h) + bx * (h * h) + cx * h
        firstFDY = ay * (h * h * h) + by * (h * h) + cy * h

        secondFDX = 6 * ax * (h * h * h) + 2 * bx * (h * h)
        secondFDY = 6 * ay * (h * h * h) + 2 * by * (h * h)

        thirdFDX = 6 * ax * (h * h * h)
        thirdFDY = 6 * ay * (h * h * h)

        # Compute points at each step
        result.append((int(pointX), int(pointY)))

        for i in range(numSteps):
            pointX += firstFDX
            pointY += firstFDY

            firstFDX += secondFDX
            firstFDY += secondFDY

            secondFDX += thirdFDX
            secondFDY += thirdFDY

            result.append((int(pointX), int(pointY)))

        return result


    def force_continuity(self, next_point: Vector2) -> Vector2:
        return next_point.project_onto(self.control_points[-1], self.control_points[-2])

class CatmullRom(Curve):
    def __init__(self, id:str, control_points: List[Vector2]):
        Curve.__init__(self, id, control_points[0])

        if len(control_points) < 3:
            raise ValueError(f"Invalid input for control points. Must have at least 3 values but list of lenght {len(control_points)} was provided: [{control_points}]")
        self.control_points = control_points

    def line_representation(self):
        return self.compute_curve_lines()

    def end_point(self):
        return self.control_points[-1]

    def compute_curve_lines(self):
        b_points = self.compute_bezier_points([(x.x, x.y) for x in self.control_points])
        ret = []
        for ii in range(0, len(b_points)):
            if ii == 0:
                continue
            else:
                start = Vector2(b_points[ii - 1][0], b_points[ii - 1][1])
                end = Vector2(b_points[ii][0], b_points[ii][1])
                ret.append(Line(self.id + f"_{ii}", start, end))
        return ret

    def compute_bezier_points(self, vertices, numPoints=None):
        if numPoints is None:
            numPoints = 30
        if numPoints < 2 or len(vertices) != 3:
            return []

        result = []




        b0x = vertices[0][0]
        b0y = vertices[0][1]
        b1x = vertices[1][0]
        b1y = vertices[1][1]
        b2x = vertices[2][0]
        b2y = vertices[2][1]
        b3x = vertices[3][0]
        b3y = vertices[3][1]

        # Compute polynomial coefficients from Bezier points
        ax = -b0x + 3 * b1x + -3 * b2x + b3x
        ay = -b0y + 3 * b1y + -3 * b2y + b3y

        bx = 3 * b0x + -6 * b1x + 3 * b2x
        by = 3 * b0y + -6 * b1y + 3 * b2y

        cx = -3 * b0x + 3 * b1x
        cy = -3 * b0y + 3 * b1y

        dx = b0x
        dy = b0y

        # Set up the number of steps and step size
        numSteps = numPoints - 1  # arbitrary choice
        h = 1.0 / numSteps  # compute our step size

        # Compute forward differences from Bezier points and "h"
        pointX = dx
        pointY = dy

        firstFDX = ax * (h * h * h) + bx * (h * h) + cx * h
        firstFDY = ay * (h * h * h) + by * (h * h) + cy * h

        secondFDX = 6 * ax * (h * h * h) + 2 * bx * (h * h)
        secondFDY = 6 * ay * (h * h * h) + 2 * by * (h * h)

        thirdFDX = 6 * ax * (h * h * h)
        thirdFDY = 6 * ay * (h * h * h)

        # Compute points at each step
        result.append((int(pointX), int(pointY)))

        for i in range(numSteps):
            pointX += firstFDX
            pointY += firstFDY

            firstFDX += secondFDX
            firstFDY += secondFDY

            secondFDX += thirdFDX
            secondFDY += thirdFDY

            result.append((int(pointX), int(pointY)))

        return result

    def force_continuity(self, next_point: Vector2) -> Vector2:
        return next_point

class CurveType(Enum):
    ARC = 1,
    CUBICBEZIER = 2,
    LINE = 3,
    CATMULLROM = 4


class CurveBuilder:

    def __init__(self, id_provider: Callable [[], str]):
        self.curves = {} # {id: curve}
        self.current_points = []
        self.current_curve_type = EnumToggleable(CurveType)
        self.current_orientation = EnumToggleable(Orientation)
        self.id_provider = id_provider

    def set_curve_type(self, curve_type: CurveType):
        self.current_curve_type.set_value(curve_type)

    def toggle_curve_type(self):
        self.current_curve_type.toggle()
        self.current_points = []

    def save_curve(self):
        new_curves = self.curves_from_points(self.current_curve_type.value, self.current_points)
        for curve in new_curves:
            self.curves[self.id_provider()] = curve
        self.current_points = []

    def add_point(self, point: Vector2):
        self.current_points.append(point)

    def remove_point(self):
        self.current_points.pop()

    def orientation(self, origin, destination) -> List[Orientation]:
        orientation = None
        if origin.x == destination.x and origin.y > destination.y:
            orientation = [Orientation.UP]
        elif origin.x == destination.x and origin.y < destination.y:
            orientation = [Orientation.DOWN]
        elif origin.x < destination.x and origin.y == destination.y:
            orientation = [Orientation.RIGHT]
        elif origin.x > destination.x and origin.y == destination.y:
            orientation = [Orientation.LEFT]
        elif origin.x > destination.x and origin.y > destination.y:
            orientation = [Orientation.UP_LEFT, Orientation.LEFT_UP]
        elif origin.x > destination.x and origin.y < destination.y:
            orientation = [Orientation.DOWN_LEFT, Orientation.LEFT_DOWN]
        elif origin.x < destination.x and origin.y > destination.y:
            orientation = [Orientation.UP_RIGHT, Orientation.RIGHT_UP]
        elif origin.x < destination.x and origin.y < destination.y:
            orientation = [Orientation.DOWN_RIGHT, Orientation.RIGHT_DOWN]
        return orientation

    def curves_from_points(self, curve_type: CurveType, points: List[Vector2]) -> (List[Curve], List[Vector2]):
        curves = []
        leftover_points = []
        if len(points) <2:
            return curves, leftover_points


        if curve_type == CurveType.LINE:
            curves = self.lines_from_points(points)
        elif curve_type == CurveType.ARC:
            curves = self.arcs_from_points(points)
        elif curve_type == CurveType.CUBICBEZIER:
            leftover_count = (len(points) - 1) % 3 if len(points) >= 4 else len(points)
            leftover_points = points[-leftover_count:] if leftover_count != 0 else leftover_points
            used_points = points[:-leftover_count] if leftover_count != 0 else points
            curves = self.cubicbeziers_from_points(used_points)
        elif curve_type == CurveType.CATMULLROM:
            curves = self.catmullrom_from_points(points)

        return curves, leftover_points

    def lines_from_points(self, points):
        lines = []
        for ii in range(len(points) - 1):
            lines.append(Line(self.id_provider(), points[ii], points[ii + 1]))
        return lines

    def arcs_from_points(self, points):
        curves = []
        for ii in range(len(points) - 1):
            orientation = self.orientation(points[ii], points[ii + 1])[0]
            if orientation in (Orientation.UP, Orientation.RIGHT, Orientation.DOWN, Orientation.LEFT):
                curves.append(Line(self.id_provider(), points[ii], points[ii + 1]))
            else:
                curves.append(Arc(self.id_provider(), orientation, points[ii],
                            Vector2(abs(points[ii + 1].x - points[ii].x) * 2, abs(points[ii + 1].y - points[ii].y) * 2))
                              )
        return curves

    def cubicbeziers_from_points(self, points):
        curves = []

        if len(points) < 4:
            return curves

        # A Cubic Bezier requires 4 control points, so operate in blocks of 4 (re-using the last each time)
        for ii in range(0, len(points) - 3, 3):
            curves.append(CubicBezier(self.id_provider(), points[ii:ii+4]))

        # curves.append(CubicBezier(self.id_provider(), points))
        return curves

    def catmullrom_from_points(self, points):
        curves = []

        curves.append(CatmullRom(self.id_provider(), points))
        return curves

    def curves_from_temp_next_points(self, next_points: List[Vector2]):
        all_points = self.current_points + next_points
        points = []
        for i in all_points:
            if i not in points:
                points.append(i)

        curves, leftovers = self.curves_from_points(self.current_curve_type.value, points)

        return curves

    def force_continuity(self, next_point: Vector2):
        curves, leftovers = self.curves_from_points(self.current_curve_type.value, self.current_points)

        if curves is None or len(curves) == 0:
            return next_point

        # Dont need to force a continuity if we are in the middle of a Bezier
        if self.current_curve_type.value == CurveType.CUBICBEZIER and len(leftovers) != 0:
            return next_point
        else:
            return curves[-1].force_continuity(next_point)


if __name__ == "__main__":
    import random as rnd
    builder = CurveBuilder(lambda: "1")

    points = []

    rnd.seed(0)
    for ii in range(16):
        points.append(Vector2(rnd.randint(0, 100), rnd.randint(0, 100)))

    curves = builder.curves_from_points(CurveType.CUBICBEZIER, points)
    print(curves)



