import math

#  Constants
t0 = 288.15
p0 = 101325
p11 = 226.32e2
t11 = 216.65
R = 287
g = 9.81


class temperature:
    @staticmethod
    def meters(altitude):
        """
        Returns temperature in Kelvin for height in altitude
        """
        if altitude > 11000:
            return 216.65
        else:
            return t0 - 6.5 * altitude / 1000

    @staticmethod
    def feet(feet):
        """
        Returns temperature in Kelvin for height in FEETS
        """
        if altitude > 36089:
            return 216.65
        else:
            return t0 - 1.98 * altitude / 1000


class presure:
    @staticmethod
    def meters(altitude):
        """
        Returns presure in Pa for height in METERS
        """
        if altitude > 11000:

            return p11 * math.exp(-g / (R * t11) * (altitude - 11000))
        else:
            return p0 * (1 - 0.0065 * altitude / t0) ** 5.2561


class density:
    @staticmethod
    def meters(altitude):
        """
        Returns density in kg/m^3 for height in altitude
        """
        density = presure.meters(altitude) / (R * temperature.meters(altitude))
        return density
