from mappers.Spline import Spline
from mappers.Curve import Curve


# Util method
def array(size):
    """
    Generates a zeroes array of the size specified.
    :param size: The size of the array.
    :return: A zeroes array of the specified size.
    """
    return [0 for _ in range(size)]


class CurveGenerator:
    @staticmethod
    def generate_curve(control_points):
        """
        Generates a list of splines that are computed from the colour coordinates provided by in the argument.
        :param control_points: The control points that the splines should be defined against. At minimum, three are
        required.
        :return: A list of splines that are generated from the control points.
        """
        if len(control_points) < 3:
            raise ValueError("Number of control points must be 3 or more.")

        delta_p = 1 / (len(control_points) - 1)
        r_set, g_set, b_set = CurveGenerator.__generate_parametrised_point_sets(delta_p, control_points)
        r_splines = CurveGenerator.__generate_spline(r_set)
        g_splines = CurveGenerator.__generate_spline(g_set)
        b_splines = CurveGenerator.__generate_spline(b_set)
        return Curve(CurveGenerator.__group_splines(r_splines, g_splines, b_splines))

    @staticmethod
    def __generate_spline(parametrised_point_set):
        """
        Generates the relevant splines for a parametrised point set.
        :param parametrised_point_set: A point set with form (p in [0, 1], x in [0, 255])
        :return: A list of Splines.
        """
        curves = CurveGenerator.__generate_curves(parametrised_point_set)
        return [
            (CurveGenerator.__convert_to_lambda_expression(curves[i]), curves[i]['x_j'])
            for i in range(len(curves))
        ]

    @staticmethod
    def __generate_parametrised_point_sets(delta_p, points):
        """
        Separates the given point set from RGB form to an ordered pair (x_n, p), where p is a parameter space
        coordinate. The original point set must be provided in the form: [(R_1, G_1, B_1), (R_2, G_2, B_2),
        (R_3, G_3, B_3), ... , (R_n, G_n, B_n)], where n is the number of control points of the curve.
        :param delta_p: The difference p_n - p_{n-1} for p in the parameter space [0, 1].
        :param points: The RGB point set to generate the curves for.
        :return: Three point sets, in the order R, G, B.
        """
        r_set = []
        g_set = []
        b_set = []
        for i in range(len(points)):
            r_set.append(points[i][0])
            g_set.append(points[i][1])
            b_set.append(points[i][2])

        return (
            CurveGenerator.__generate_parametrised_point_set(delta_p, r_set),
            CurveGenerator.__generate_parametrised_point_set(delta_p, g_set),
            CurveGenerator.__generate_parametrised_point_set(delta_p, b_set)
        )

    @staticmethod
    def __generate_parametrised_point_set(delta_p, points):
        """
        Collects the points given and creates ordered pairs of (p, x), where p is a monotonic increasing point set in
        the [0, 1] parameter space.
        :param delta_p: The difference p_n - p_{n-1} for p in the parameter space [0, 1].
        :param points: The one dimensional point set to be mapped.
        :return:
        """
        parametrised_set = []
        p = delta_p
        for i in range(len(points)):
            parametrised_set.append((p, points[i]))
            p += delta_p

        return parametrised_set

    @staticmethod
    def __generate_curves(point_set):
        """
        Algorithm taken from Wikipedia: (https://en.wikipedia.org/wiki/Spline_(mathematics)) - § Algorithm for computing
        natural cubic splines. Generates a spline curve for each specific point set.
        :param point_set: The (x_n, p) form point set as the domain for the spline curve.
        :return: A collection of tuples for the coefficients of the cubic splines.
        """
        a = [point_set[i][1] for i in range(len(point_set))]
        b = array(len(point_set) - 1)
        d = array(len(point_set) - 1)
        h = [point_set[i + 1][0] - point_set[i][0] for i in range(len(point_set) - 1)]
        alpha = array(len(point_set) - 1)
        for i in range(1, len(point_set) - 1):
            ((3 / h[i]) * (a[i + 1] - a[i])) - ((3 / h[i - 1]) * (a[i] - a[i - 1]))
        c = array(len(point_set))
        l = array(len(point_set))
        l[0] = 0
        mu = array(len(point_set))
        z = array(len(point_set))
        for i in range(1, len(point_set) - 1):
            l[i] = 2 * (point_set[i + 1][0] - point_set[i - 1][0]) - h[i - 1] * mu[i - 1]
            mu[i] = h[i] / l[i]
            z[i] = (alpha[i] - h[i - 1] * z[i - 1]) / l[i]
        l[len(point_set) - 1] = 1
        z[len(point_set) - 1] = 0
        c[len(point_set) - 1] = 0
        for j in range(len(point_set) - 2, 0, -1):
            c[j] = z[j] - mu[j] * c[j + 1]
            b[j] = ((a[j + 1] - a[j]) / h[j]) - ((h[j] * (c[j + 1] * 2 * c[j])) / 3)
            d[j] = (c[j + 1] - c[j]) / (3 * h[j])

        return [
            {
                'a': a[i],
                'b': b[i],
                'c': c[i],
                'd': d[i],
                'x_j': point_set[i][0]
            }
            for i in range(len(point_set) - 1)
        ]

    @staticmethod
    def __convert_to_lambda_expression(curve):
        """
        Converts the coefficients in the splines list to actual lambda expressions that can be evaluated directly. The
        idea is that the list of coefficients gets converted into a list of function pointers, each of which corresponds
        to one of the functions in the piecewise definition of the spline.
        :param curve: The list of coefficients for the spline.
        :return: A lambda expression (function pointer) that correspond to the spline.
        """
        return lambda x: (
            CurveGenerator.__clamp_as_int(
                curve['a']
                + curve['b'] * (x - curve['x_j'])
                + curve['c'] * (x - curve['x_j']) ** 2
                + curve['d'] * (x - curve['x_j']) ** 3
            )
        )

    @staticmethod
    def __clamp_as_int(number):
        """
        Converts number to an integer value in the range [0, 255].
        :param number: The number to be clamped.
        :return: The normalised clamped version of the number.
        """
        number = int(number)
        if number < 0:
            number = 0
        elif number > 255:
            number = 255

        return number

    @staticmethod
    def __group_splines(r_splines, g_splines, b_splines):
        """
        Groups the three function pointer list elements into single element list, which can then be used for evaluating
        individual data points.
        :param r_splines: The splines associated with the red pixel values.
        :param g_splines: The splines associated with the green pixel values.
        :param b_splines: The splines associated with the blue pixel values.
        :return: A grouped element list, with each element being a 4 tuple, in the form: (R, G, B, x_j).
        """
        assert len(r_splines) == len(g_splines) == len(b_splines)
        return [
            (Spline(expression=r_splines[i][0], point=r_splines[i][1]),
             Spline(expression=g_splines[i][0], point=g_splines[i][1]),
             Spline(expression=b_splines[i][0], point=b_splines[i][1]))
            for i in range(len(r_splines))
        ]
