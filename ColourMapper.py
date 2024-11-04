from transformers.OutputTransformer import ConversionCodes
from transformers.OutputTransformer import OutputTransformer
from transformers.InputTransformer import InputTransformer
from mappers.CurveGenerator import CurveGenerator
import numpy as np


class ColourMapper:
    def __init__(self):
        self.curve = None

    def generate_map(self, colours):
        """
        Generates the mapping curve from the data's space, to the finite RGB 3-space.
        :param colours: The colours that define the control points for the mapping.
        """
        if len(colours) < 3:
            raise ValueError('Too few colours provided to generate colour map.')
        self.curve = CurveGenerator.generate_curve(colours)

    def map(self, data, data_type='scalar', output_space='rgb', raw_output=True):
        """
        Maps the data in its original space to the RGB 3-space using the curve generated from colours provided to the
        object. To map scalar data to the colour space, the data_type should be set to 'scalar'. If vector data is
        provided, then use 'vector' for data_type. The mapping can be provided in multiple different types for the
        output colour space. The codes for the output space are 'rgb': Red Green Blue, 'bgr': Blue Green Red,
        'hls': Hue Luminescence Saturation, 'hsv': Hue Luminescence Value, 'ycbcr': Luma Chroma Blue Chroma Red.
        :param data: The data to be mapped. Can be either scalar or vector.
        :param data_type: The input data type, either scalar or vector.
        :param output_space: The output colour space, either RGB, BGR, HSV, HLS, YCBCR.
        :param raw_output: Whether the output should be provided as a raw value, or a scaled value in the range [0, 1].
        :return:
        """
        if data_type is not ('scalar' or 'vector'):
            raise ValueError('Unsupported input data type. Supported data types are n-dimensional vectors and scalars.')
        match output_space:
            case 'rgb':
                output_space = ConversionCodes.RGB
            case 'bgr':
                output_space = ConversionCodes.BGR
            case 'hls':
                output_space = ConversionCodes.HLS
            case 'hsv':
                output_space = ConversionCodes.HSV
            case 'ycbcr':
                output_space = ConversionCodes.YCBCR
            case _:
                raise ValueError('Unrecognised output colour space.')
        parameterised_data = InputTransformer.convert(data, data_type)
        output = np.array(parameterised_data.shape)
        for i in range(output.shape[0]):
            for j in range(output.shape[1]):
                output[i][j] = self.curve.compute_pixel_coordinate(parameterised_data[i][j])

        return OutputTransformer.process(output, output_space, raw_output)
