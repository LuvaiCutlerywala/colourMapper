import numpy as np


class InputTransformer:
    @staticmethod
    def convert(data, data_type):
        """
        Converts the data from the original format to the parameter space.
        :param data: The original data.
        :param data_type: The type of the original data, can either be vector or scalar.
        :return: The data converted from its original space to parameter space.
        """
        data = np.asarray(data)
        if data_type == 'vector':
            data = InputTransformer.__convert_vector_data_to_parameter_space(data)
        else:
            data = InputTransformer.__convert_scalar_data_to_parameter_space(data)

        return data

    @staticmethod
    def __convert_scalar_data_to_parameter_space(data):
        """
        Converts scalar data to parameter space.
        :param data: The data provided by the user.
        :return: The data converted from its original scalar space to parameter space.
        """
        data_min = np.min(data)
        if data_min < 0:
            data += np.abs(data_min)

        return data / np.max(data)

    @staticmethod
    def __convert_vector_data_to_parameter_space(data):
        """
        Converts vector data to parameter space.
        :param data: The data provided by the user.
        :return: The data converted from its original vector space to parameter space.
        """
        magnitude_matrix = InputTransformer.__convert_cartesian_space_to_magnitude_matrix(data)
        magnitude_matrix = np.asarray(magnitude_matrix)
        return magnitude_matrix / np.max(magnitude_matrix)

    @staticmethod
    def __convert_cartesian_space_to_magnitude_matrix(data):
        """
        Converts a matrix of cartesian vectors to their corresponding magnitude matrix.
        :param data: The cartesian vector matrix.
        :return: The resulting magnitude matrix.
        """
        output = []
        for i in range(len(data)):
            row = []
            for j in range(len(data[i])):
                row.append(np.sqrt(data[i][j].dot(data[i][j])))
            output.append(row)

        return output
