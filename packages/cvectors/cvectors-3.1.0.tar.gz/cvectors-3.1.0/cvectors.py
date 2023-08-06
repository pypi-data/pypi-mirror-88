"""A package for using complex numbers as 2D vectors."""
from __future__ import annotations

import cmath


def convert_angle(angle, /, unit: str):
    """Convert an angle to radians."""
    unit = unit.lower()
    if unit in {"d", "deg", "degrees", "degree", "°"}:
        return angle * cmath.tau / 360
    if unit in {"r", "", None, "rad", "radian", "radians"}:
        return angle
    if unit in {"g", "grad", "gradians", "gradian", "gons", "gon", "grades", "grade"}:
        return angle * cmath.tau / 400
    if unit in {"mins", "min", "minutes", "minute", "'", "′"}:
        return angle * cmath.tau / 21600
    if unit in {"secs", "sec", "seconds", "seconds", '"', "″"}:
        return angle * cmath.tau / 1296000
    if unit in {"turn", "turns"}:
        return angle * cmath.tau
    raise ValueError(f"Invalid angle unit: '{unit}'")


def _object_to_xy(obj, /) -> tuple:
    """Convert an object to an (x, y) tuple."""
    # Deal with objects with x and y attributes
    try:
        return (obj.x, obj.y)
    except AttributeError:
        pass
    # Deal with iterables
    try:
        iterable = iter(obj)
        try:
            x = next(iterable)
            y = next(iterable)
        except StopIteration:
            raise ValueError("Iterable is too short to create Vector")
        try:
            next(iterable)
            raise ValueError("Iterable is too long to create Vector")
        except StopIteration:
            return (x, y)
    except TypeError:
        raise TypeError(
            "Single argument Vector must be Vector, complex, iterable or have x and y attributes"
        )


class Vector(complex):
    """A two-dimensional vector."""

    def __new__(cls, /, x=None, y=None, *, r=None, theta=None, angle_unit: str = "rad"):
        if x is None:
            if y is not None:
                raise ValueError("Must give x to create Vector if y is given")
            # Create Vector from polar arguments
            if r == 0:
                return super().__new__(cls, 0)
            if r is None or theta is None:
                raise ValueError("Insufficient information to create Vector")
            return super().__new__(cls, cmath.rect(r, convert_angle(theta, angle_unit)))
        if r is not None or theta is not None:
            raise ValueError(
                "Cannot create Vector from mixed rectangular and polar arguments"
            )
        if y is None:
            # Create Vector from a single argument using the
            # implementation complex provides
            try:
                return super().__new__(cls, x)
            except TypeError:
                # Get x and y values using our implementation
                x, y = _object_to_xy(x)

        # Create Vector from x and y
        try:
            return super().__new__(cls, x, y)
        except TypeError:
            raise TypeError("x and y values must be numeric to create Vector")

    def dot(self, other: Vector, /) -> float:
        """Return the dot product of self and other."""
        return self.real * other.real + self.imag * other.imag

    def perp_dot(self, other: Vector, /) -> float:
        """
        Return the perp dot product of self and other.

        This is the signed area of the parallelogram they define. It is
        also one of the 'cross products' that can be defined on 2D
        vectors.
        """
        return self.real * other.imag - self.imag * other.real

    def perp(self, /) -> Vector:
        """
        Return the Vector, rotated anticlockwise by pi / 2.

        This is one of the 'cross products' that can be defined on 2D
        vectors. Use -Vector.perp() for a clockwise rotation.
        """
        return Vector(-self.imag, self.real)

    def rotate(self, angle, /, unit="rad") -> Vector:
        """
        Return a self, rotated by angle anticlockwise.

        Use negative angles for a clockwise rotation.
        """
        angle = convert_angle(angle, unit)
        return Vector(r=self.r, theta=self.theta + angle)

    def hat(self, /) -> Vector:
        """Return a Vector with the same direction, but unit length."""
        return self / abs(self)

    def rec(self, /) -> tuple[float, float]:
        """Get the vector as (x, y)."""
        return (self.real, self.imag)

    def pol(self, /) -> tuple[float, float]:
        """Get the vector as (r, theta)."""
        return cmath.polar(self)

    def __repr__(self, /):
        return f"{self.__class__.__name__}({self.real}, {self.imag})"

    def __str__(self, /):
        return f"({self.real} {self.imag})"

    def __len__(self, /):
        return 2

    def __getitem__(self, key, /):
        return self.rec()[key]

    def __contains__(self, item, /):
        return item == self.real or item == self.imag

    def __iter__(self, /):
        yield self.real
        yield self.imag

    def __reversed__(self, /):
        yield self.imag
        yield self.real

    def __round__(self, ndigits=0, /) -> tuple:
        return (round(self.real, ndigits), round(self.imag, ndigits))

    def __add__(self, other, /) -> Vector:
        return Vector(self.real + other.real, self.imag + other.imag)

    def __sub__(self, other, /) -> Vector:
        return Vector(self.real - other.real, self.imag - other.imag)

    def __mul__(self, other, /) -> Vector:
        return Vector(super().__mul__(other))

    def __truediv__(self, other, /) -> Vector:
        return Vector(super().__truediv__(other))

    def __pow__(self, value, mod=None, /) -> Vector:
        return Vector(super().__pow__(value, mod))

    __radd__ = __add__
    __rsub__ = __sub__
    __rmul__ = __mul__
    __rtruediv__ = __truediv__
    __rpow__ = __pow__

    @property
    def x(self) -> float:
        """The horizontal component of the vector."""
        return self.real

    @property
    def y(self) -> float:
        """The vertical component of the vector."""
        return self.imag

    @property
    def r(self) -> float:
        """The radius of the vector."""
        return abs(self)

    @property
    def theta(self) -> float:
        """
        The angle of the vector, anticlockwise from the horizontal.

        Negative values are clockwise. Returns values in the range
        [-pi, pi]. See documentation of cmath.phase for details.
        """
        return cmath.phase(self)
