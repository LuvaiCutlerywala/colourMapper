import numpy as np
import cv2
from enum import Enum


class ConversionCodes(Enum):
    """
    Defines the ranges for colour space dimensions. The colour space are finite dimensional bounded spaces. They are not
    closed.
    """
    BGR = ((0, 255), (0, 255), (0, 255))
    RGB = ((0, 255), (0, 255), (0, 255))
    HSV = ((0, 360), (0, 100), (0, 100))
    HLS = ((0, 360), (0, 100), (0, 100))
    YCBCR = ((16, 235), (16, 240), (16, 240))


class OutputTransformer:
    @staticmethod
    def process(pixel_matrix, conversion_code, raw=True):
        """
        Processes the output pixel matrix into one of six output types. The supported output types are HLS (Hue,
        Lightness, Saturation), RGB (Red, Green, Blue), BGR (Blue, Green, Red), HSV (Hue, Saturation, Value), YCbCr
        (Luma, Chroma Blue, Chroma Red). If the raw parameter is given as true, then the raw values are returned. If
        false, a scaled value is returned, where each number is given as a percentage of the value from min to max.
        :param raw: True if the raw values need to be used, False if scaled values need to be used.
        :param pixel_matrix: The matrix of 3 tuples that represents the colour coded set for the data.
        :param conversion_code: The format for the colour output required.
        :return:
        """
        if conversion_code == ConversionCodes.BGR:
            return OutputTransformer.__convert_to_bgr(pixel_matrix)
        elif conversion_code == ConversionCodes.HSV:
            return OutputTransformer.__convert_to_hsv(pixel_matrix)
        elif conversion_code == ConversionCodes.YCBCR:
            return OutputTransformer.__convert_to_hsv(pixel_matrix)
        elif conversion_code == ConversionCodes.HLS:
            return OutputTransformer.__convert_to_hls(pixel_matrix)

        if not raw:
            pixel_matrix = OutputTransformer.__convert_to_scaled_form(pixel_matrix, conversion_code)

        return pixel_matrix

    @staticmethod
    def __convert_to_hsv(pixel_matrix):
        """
        Converts the colour data from RGB to HSV space.
        :param pixel_matrix: The colour data matrix.
        :return: The colour data matrix with converted values.
        """
        return cv2.cvtColor(np.asarray(pixel_matrix), cv2.COLOR_RGB2HSV)

    @staticmethod
    def __convert_to_bgr(pixel_matrix):
        """
        Converts the colour data from RGB to BGR space.
        :param pixel_matrix: The colour data matrix.
        :return: The colour data matrix with converted values.
        """
        return cv2.cvtColor(np.asarray(pixel_matrix), cv2.COLOR_RGB2BGR)

    @staticmethod
    def __convert_to_ycbcr(pixel_matrix):
        """
        Converts the colour data from RGB to YCbCr space.
        :param pixel_matrix: The colour data matrix.
        :return: The colour data matrix with converted values.
        """
        return cv2.cvtColor(np.asarray(pixel_matrix), cv2.COLOR_RGB2YCrCb)

    @staticmethod
    def __convert_to_hls(pixel_matrix):
        """
        Converts the colour data from the RGB to HLS space.
        :param pixel_matrix: The colour data matrix.
        :return: The colour data matrix with converted values.
        """
        return cv2.cvtColor(np.asarray(pixel_matrix), cv2.COLOR_RGB2HLS)

    @staticmethod
    def __convert_to_scaled_form(pixel_matrix, conversion_code):
        """
        Converts the colour data matrix from raw values to scaled values in the interval [0, 1].
        :param pixel_matrix:
        :param conversion_code:
        :return:
        """
        for i in range(len(pixel_matrix)):
            for j in range(len(pixel_matrix[i])):
                pixel_matrix[i][j] = OutputTransformer.__calculate_normalised_form(pixel_matrix[i][j], conversion_code)

        return pixel_matrix

    @staticmethod
    def __calculate_normalised_form(pixel, normalisation_factor):
        """
        Normalises the pixel value using the appropriate scaling values to the interval [0, 1], determined from the
        range of colour space dimensions.
        :param pixel: The pixel values.
        :param normalisation_factor: The ranges for colour space dimensions.
        :return: The scaled values from the finite dimension space to space [0, 1]^3.
        """
        value_range = [normalisation_factor[i][1] - normalisation_factor[i][0]
                       for i in range(len(normalisation_factor))]
        for i in range(len(pixel)):
            pixel[i] = pixel[i]/value_range[i]

        return pixel
