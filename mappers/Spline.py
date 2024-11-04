class Spline:
    def __init__(self, point, expression):
        self.point = point
        self.expression = expression

    def get_point(self):
        """
        Returns the point which represents the upper limit of the splines' domain.
        :return: The supremum of the spline's domain.
        """
        return self.point

    def compute(self, parameter):
        """
        Evaluates the spline at the given parameter. Assumption is made that the spline is valid for the parameter used.
        :param parameter: The argument of the spline.
        :return: The value of the spline at the argument.
        """
        return self.expression(parameter)
