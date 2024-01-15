from abc import ABC, abstractmethod

END = '\033[0'
START = '\033[1;38;2'
MODE = 'm'


class ComputerColor(ABC):

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def __mul__(self, c):
        pass

    @abstractmethod
    def __rmul__(self, c):
        pass


class Color(ComputerColor):
    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

    def __str__(self):
        return f'{START};{self.red};{self.green};{self.blue}{MODE}●{END}{MODE}'

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if not (isinstance(other, Color) or issubclass(other, Color)):
            return NotImplemented

        if (
            self.red == other.red
            and self.green == other.green
            and self.blue == other.blue
        ):
            return True
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    @staticmethod
    def mix_colors(color1, color2):
        return min(color1 + color2, 255)

    def __add__(self, other):
        if isinstance(other, Color) or issubclass(other, Color):
            return Color(
                self.mix_colors(self.red, other.red),
                self.mix_colors(self.green, other.green),
                self.mix_colors(self.blue, other.blue)
            )
        else:
            return NotImplemented

    def __hash__(self):
        return hash((self.red, self.green, self.blue))

    def __mul__(self, c):
        if isinstance(c, float) or isinstance(c, int):
            if 0.0 <= c <= 1.0:
                cl = -256 * (1 - c)
                F = 259 / 255 * (cl + 255) / (259 - cl)
                red = int(F * (self.red - 128) + 128)
                green = int(F * (self.green - 128) + 128)
                blue = int(F * (self.blue - 128) + 128)
                return Color(red, green, blue)
            else:
                raise ValueError('c must be between 0 and 1')
        else:
            return NotImplemented

    def __rmul__(self, c):
        return self.__mul__(c)
