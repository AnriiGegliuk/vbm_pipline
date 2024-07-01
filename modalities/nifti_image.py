import math
import numpy as np
import matplotlib.pyplot as plt
from nibabel import load
from nibabel import save
from nibabel import Nifti1Image
from nilearn.plotting import plot_anat


class NiftiImage:
    """
    Handle a NIfTI1-format image data.
    """

    def __init__(self, image_file_path: str):
        """
        [arguments]
        file_path: NIfTI1-format image file path.
        """
        self.image_file_path = image_file_path

        # Create the NIfTI image object from the file.
        self.img = load(image_file_path)

    @property
    def image_data(self):
        """
        Return the raw image data without affine transformation.
        """
        return self.img.get_fdata()

    def update_affine_matrix(self, alignment_params, save_file_path: str = None):
        """
        Calculate a new affine transformation matrix with alignment parameters,
        and update the NIfTI image object with the matrix.
        """

        # Calculate a new affine transformation matrix.
        current_matrix = self.__create_affine_matrix_from_params(alignment_params)
        new_affine_matrix = np.dot(current_matrix, self.img.affine)

        # Update the NIfTI image object with the new matrix.
        self.img = Nifti1Image(self.img.get_fdata(), new_affine_matrix, self.img.header)

    def __create_affine_matrix_from_params(self, params):
        """
        Create an affine transformation matrix from the following alignment parameters:
          0: X translation
          1: Y translation
          2: Z translation
          3: X rotation (pitch (radians))
          4: Y rotation (roll (radians))
          5: Z rotation (yaw (radians))
          6: X scaling
          7: Y scaling
          8: Z scaling
          9: X affine
          10: Y affine
          11: Z affine.
        The implementation is based on the spm_matrix() function of SPM12.
        """

        translation_matrix = np.array([[1, 0, 0, params[0]],
                                       [0, 1, 0, params[1]],
                                       [0, 0, 1, params[2]],
                                       [0, 0, 0, 1]])

        # Create the rotation matrix.
        rotation_matrix_1 = np.array([[1, 0, 0, 0],
                                      [0, math.cos(params[3]), math.sin(params[3]), 0],
                                      [0, -math.sin(params[3]), math.cos(params[3]), 0],
                                      [0, 0, 0, 1]])

        rotation_matrix_2 = np.array([[math.cos(params[4]), 0, math.sin(params[4]), 0],
                                      [0, 1, 0, 0],
                                      [-math.sin(params[4]), 0, math.cos(params[4]), 0],
                                      [0, 0, 0, 1]])

        rotation_matrix_3 = np.array([[math.cos(params[5]), math.sin(params[5]), 0, 0],
                                      [-math.sin(params[5]), math.cos(params[5]), 0, 0],
                                      [0, 0, 1, 0],
                                      [0, 0, 0, 1]])

        rotation_matrix = rotation_matrix_1 @ rotation_matrix_2 @ rotation_matrix_3

        scaling_matrix = np.array([[params[6], 0, 0, 0],
                                   [0, params[7], 0, 0],
                                   [0, 0, params[8], 0],
                                   [0, 0, 0, 1]])

        shear_matrix = np.array([[1, params[9], params[10], 0],
                                 [0, 1, params[11], 0],
                                 [0, 0, 1, 0],
                                 [0, 0, 0, 1]])

        affine_matrix = translation_matrix @ rotation_matrix @ scaling_matrix @ shear_matrix

        return affine_matrix

    def save(self, save_file_path: str = None):

        # Overwrite the NIfTI file if save_file_path is not specified.
        if save_file_path is None:
            save_file_path = self.image_file_path

        save(self.img, save_file_path)

    
    def plot_with_crosshair(self, crosshair_position):
        """
        Plot the NIfTI image with a crosshair at the specified position.
        """
        display = plot_anat(self.img)
        display.add_markers([crosshair_position], marker_color='r', marker_size=100)
        plt.show()


# import numpy as np
# import matplotlib.pyplot as plt
# from nibabel import load, save, Nifti1Image
# from nilearn.plotting import plot_anat

# class NiftiImage:
#     """
#     Handle a NIfTI1-format image data.
#     """

#     def __init__(self, image_file_path: str):
#         """
#         Initialize the NIfTI image object from the file.
#         :param image_file_path: NIfTI1-format image file path.
#         """
#         self.image_file_path = image_file_path
#         self.img = load(image_file_path)

#     @property
#     def image_data(self):
#         """
#         Return the raw image data without affine transformation.
#         """
#         return self.img.get_fdata()

#     def update_affine_matrix(self, alignment_params, save_file_path: str = None):
#         """
#         Update the NIfTI image object with a new affine transformation matrix based on alignment parameters.
#         :param alignment_params: List of alignment parameters for affine transformation.
#         :param save_file_path: Optional path to save the updated image.
#         """
#         new_affine_matrix = self._create_affine_matrix_from_params(alignment_params)
#         updated_affine = np.dot(new_affine_matrix, self.img.affine)
#         self.img = Nifti1Image(self.img.get_fdata(), updated_affine, self.img.header)
#         if save_file_path:
#             self.save(save_file_path)

#     def _create_affine_matrix_from_params(self, params):
#         """
#         Create an affine transformation matrix from alignment parameters.
#         :param params: List of alignment parameters.
#         :return: Affine transformation matrix.
#         """
#         translation_matrix = np.eye(4)
#         translation_matrix[:3, 3] = params[:3]

#         rotation_matrix = self._create_rotation_matrix(params[3:6])
#         scaling_matrix = np.diag([params[6], params[7], params[8], 1])
#         shear_matrix = np.eye(4)
#         shear_matrix[0, 1] = params[9]
#         shear_matrix[0, 2] = params[10]
#         shear_matrix[1, 2] = params[11]

#         return translation_matrix @ rotation_matrix @ scaling_matrix @ shear_matrix

#     def _create_rotation_matrix(self, angles):
#         """
#         Create a rotation matrix from the given angles.
#         :param angles: List of rotation angles in radians.
#         :return: Rotation matrix.
#         """
#         pitch, roll, yaw = angles

#         Rx = np.array([[1, 0, 0, 0],
#                        [0, np.cos(pitch), -np.sin(pitch), 0],
#                        [0, np.sin(pitch), np.cos(pitch), 0],
#                        [0, 0, 0, 1]])

#         Ry = np.array([[np.cos(roll), 0, np.sin(roll), 0],
#                        [0, 1, 0, 0],
#                        [-np.sin(roll), 0, np.cos(roll), 0],
#                        [0, 0, 0, 1]])

#         Rz = np.array([[np.cos(yaw), -np.sin(yaw), 0, 0],
#                        [np.sin(yaw), np.cos(yaw), 0, 0],
#                        [0, 0, 1, 0],
#                        [0, 0, 0, 1]])

#         return Rz @ Ry @ Rx

#     def save(self, save_file_path: str = None):
#         """
#         Save the NIfTI image.
#         :param save_file_path: Optional path to save the updated image.
#         """
#         if save_file_path is None:
#             save_file_path = self.image_file_path
#         save(self.img, save_file_path)

#     def plot_with_crosshair(self, crosshair_position_vox):
#         """
#         Plot the NIfTI image with a crosshair at the specified voxel position.
#         :param crosshair_position_vox: Voxel coordinates for the crosshair.
#         """
#         # Convert voxel coordinates to world coordinates using the affine matrix
#         crosshair_position_world = np.dot(self.img.affine, np.append(crosshair_position_vox, 1))[:3]

#         display = plot_anat(self.img)
#         display.add_markers([crosshair_position_world], marker_color='r', marker_size=100)
#         plt.show()