class Curve:
    def __init__(self, splines):
        self.splines = splines
        self.ranges = []
        prev = 0
        for i in range(len(splines)):
            self.ranges.append((prev, splines[i][0].get_point()))
            prev = splines[i][0].get_point()

    def get_ranges(self):
        """
        Returns the ranges that the splines are defined over.
        :return: The domains of the splines.
        """
        return self.ranges

    def get_splines(self):
        """
        Returns the splines.
        :return: The splines.
        """
        return self.splines

    def compute_pixel_coordinate(self, parameter):
        """
        Checks the range through which the corresponding parameter fits, and the computes the RGB value at that point
        using the splines defined for the corresponding point.
        :param parameter: The element from the domain space of [0, 1].
        :return: A tuple in the form (R, G, B), which returns the mapped pixel value.
        """
        for i in range(len(self.ranges)):
            if self.ranges[i][0] <= parameter <= self.ranges[i][1]:
                return [
                    self.splines[i][0].compute(parameter),
                    self.splines[i][1].compute(parameter),
                    self.splines[i][2].compute(parameter)
                ]
