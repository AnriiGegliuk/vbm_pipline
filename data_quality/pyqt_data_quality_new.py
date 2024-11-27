# import os
# import nibabel as nib
# import numpy as np
# import pyqtgraph as pg
# from pyqtgraph.Qt import QtCore, QtGui, QtWidgets
# import tkinter as tk
# from tkinter import filedialog, messagebox

# class MRISegmentValidator(QtWidgets.QWidget):
#     def __init__(self, root_dir, segment_folder='3_segment'):
#         super().__init__()
#         self.root_dir = root_dir
#         self.segment_folder = segment_folder
#         self.current_image_type = "rc1"
#         self.current_subject = None
#         self.file_paths = self.collect_nifti_files()
#         self.current_file_idx = 0
#         self.segment_validations = {}
#         self.processed_subjects = set()
#         self.init_ui()
#         self.load_next_image()

#     def init_ui(self):
#         self.setWindowTitle('MRI Segment Validator')
#         self.resize(1200, 800)  # Set the default window size

#         layout = QtWidgets.QVBoxLayout()
#         top_layout = QtWidgets.QHBoxLayout()

#         # Add buttons for rc1, rc2, and rc3
#         self.rc1_button = QtWidgets.QPushButton('rc1')
#         self.rc2_button = QtWidgets.QPushButton('rc2')
#         self.rc3_button = QtWidgets.QPushButton('rc3')

#         self.rc1_button.clicked.connect(lambda: self.set_image_type('rc1'))
#         self.rc2_button.clicked.connect(lambda: self.set_image_type('rc2'))
#         self.rc3_button.clicked.connect(lambda: self.set_image_type('rc3'))

#         top_layout.addWidget(self.rc1_button)
#         top_layout.addWidget(self.rc2_button)
#         top_layout.addWidget(self.rc3_button)

#         layout.addLayout(top_layout)

#         # Add subject name and image type display
#         self.subject_name_label = QtWidgets.QLabel("Subject Name: ")
#         self.subject_name_label.setFixedHeight(20)  # Adjust height
#         layout.addWidget(self.subject_name_label)
#         self.image_type_label = QtWidgets.QLabel("Image Type: ")
#         self.image_type_label.setFixedHeight(20)  # Adjust height
#         layout.addWidget(self.image_type_label)

#         main_layout = QtWidgets.QHBoxLayout()

#         # Add subject list
#         self.subject_list = QtWidgets.QListWidget()
#         self.subject_list.setFixedWidth(200)  # Adjust width
#         self.subject_list.itemClicked.connect(self.on_subject_selected)
#         main_layout.addWidget(self.subject_list)

#         # Create layout for image views
#         img_layout = QtWidgets.QVBoxLayout()
#         self.view_coronal = pg.ImageView()
#         self.view_axial = pg.ImageView()

#         # Remove the scroll bars
#         self.view_coronal.ui.histogram.hide()
#         self.view_coronal.ui.roiBtn.hide()
#         self.view_coronal.ui.menuBtn.hide()

#         self.view_axial.ui.histogram.hide()
#         self.view_axial.ui.roiBtn.hide()
#         self.view_axial.ui.menuBtn.hide()

#         img_layout.addWidget(self.view_coronal)
#         img_layout.addWidget(self.view_axial)

#         main_layout.addLayout(img_layout)
#         layout.addLayout(main_layout)

#         # Add sliders
#         self.slider_coronal = QtWidgets.QSlider(QtCore.Qt.Horizontal)
#         self.slider_axial = QtWidgets.QSlider(QtCore.Qt.Horizontal)

#         layout.addWidget(self.slider_coronal)
#         layout.addWidget(self.slider_axial)

#         self.valid_button = QtWidgets.QPushButton('Valid')
#         self.invalid_button = QtWidgets.QPushButton('Invalid')

#         self.valid_button.clicked.connect(lambda: self.validate_segmentation(True))
#         self.invalid_button.clicked.connect(lambda: self.validate_segmentation(False))

#         layout.addWidget(self.valid_button)
#         layout.addWidget(self.invalid_button)

#         # Radio button for switching segment folders
#         self.segment_radio = QtWidgets.QRadioButton("Switch to 2_segment")
#         self.segment_radio.toggled.connect(self.switch_segment_folder)
#         layout.addWidget(self.segment_radio)

#         self.setLayout(layout)

#         self.slider_coronal.valueChanged.connect(lambda val: self.on_scroll(val, 0))
#         self.slider_axial.valueChanged.connect(lambda val: self.on_scroll(val, 1))

#         self.populate_subject_list()

#     def collect_nifti_files(self):
#         file_paths = []
#         for subject in sorted(os.listdir(self.root_dir)):
#             subject_dir = os.path.join(self.root_dir, subject, 'segmentation', self.segment_folder, 'dartel_input_images')
#             if os.path.isdir(subject_dir):
#                 rc_files = [os.path.join(subject_dir, f) for f in sorted(os.listdir(subject_dir)) if f.startswith('rc')]
#                 file_paths.extend(rc_files)
#         return file_paths

#     def load_image(self, file_path):
#         img = nib.load(file_path)
#         data = img.get_fdata()
#         return data

#     def load_next_image(self):
#         if self.current_file_idx >= len(self.file_paths):
#             messagebox.showinfo("Info", "Validation completed")
#             self.save_results()
#             self.close()
#             return
#         while self.current_file_idx < len(self.file_paths):
#             file_path = self.file_paths[self.current_file_idx]
#             if self.current_image_type not in file_path:
#                 self.current_file_idx += 1
#                 continue
#             subject_name = self.get_subject_name(file_path)
#             if subject_name in self.processed_subjects:
#                 self.current_file_idx += 1
#             else:
#                 self.img_data = self.load_image(file_path)
#                 self.slice_indices = [self.img_data.shape[0] // 2, self.img_data.shape[1] // 2]
#                 self.update_sliders()
#                 self.display_image()
#                 self.update_labels()
#                 break

#     def display_image(self):
#         coronal_slice = np.rot90(self.img_data[self.slice_indices[0], :, :])
#         axial_slice = np.rot90(self.img_data[:, self.slice_indices[1], :])

#         self.view_coronal.setImage(coronal_slice)
#         self.view_axial.setImage(axial_slice)

#     def update_labels(self):
#         subject_name = self.get_subject_name(self.file_paths[self.current_file_idx])
#         self.subject_name_label.setText(f"Subject Name: {subject_name}")
#         self.image_type_label.setText(f"Image Type: {self.current_image_type}")

#     def get_subject_name(self, file_path):
#         parts = file_path.split(os.sep)
#         for i, part in enumerate(parts):
#             if part == 'segmentation':
#                 return parts[i-1]
#         return "Unknown Subject"

#     def on_scroll(self, val, axis):
#         self.slice_indices[axis] = int(val)
#         self.display_image()

#     def validate_segmentation(self, label):
#         subject_name = self.get_subject_name(self.file_paths[self.current_file_idx])
#         if not label:
#             # If any image is invalid, mark all images for this subject as invalid
#             for file_path in self.file_paths:
#                 if subject_name in file_path:
#                     self.segment_validations[file_path] = False
#                     self.processed_subjects.add(subject_name)
#         else:
#             # If marked as valid, only mark this specific image as valid
#             self.segment_validations[self.file_paths[self.current_file_idx]] = True

#         # Move to the next image
#         self.current_file_idx += 1
#         self.load_next_image()

#     def save_results(self):
#         with open(os.path.join(self.root_dir, 'validation_results.txt'), 'w') as f:
#             for file, result in self.segment_validations.items():
#                 f.write(f"{file}: {'Valid' if result else 'Invalid'}\n")

#     def update_sliders(self):
#         self.slider_coronal.setMaximum(self.img_data.shape[0] - 1)
#         self.slider_axial.setMaximum(self.img_data.shape[1] - 1)

#         self.slider_coronal.setValue(self.slice_indices[0])
#         self.slider_axial.setValue(self.slice_indices[1])

#     def switch_segment_folder(self):
#         if self.segment_radio.isChecked():
#             self.segment_folder = '2_segment'
#         else:
#             self.segment_folder = '3_segment'
#         self.file_paths = self.collect_nifti_files()
#         self.current_file_idx = 0
#         self.load_next_image()

#     def set_image_type(self, image_type):
#         self.current_image_type = image_type
#         if self.current_subject:
#             self.file_paths = self.collect_nifti_files_for_subject(self.current_subject)
#         self.current_file_idx = 0
#         self.load_next_image()

#     def collect_nifti_files_for_subject(self, subject_name):
#         file_paths = []
#         subject_dir = os.path.join(self.root_dir, subject_name, 'segmentation', self.segment_folder, 'dartel_input_images')
#         if os.path.isdir(subject_dir):
#             rc_files = [os.path.join(subject_dir, f) for f in sorted(os.listdir(subject_dir)) if f.startswith('rc')]
#             file_paths.extend(rc_files)
#         return file_paths

#     def on_subject_selected(self, item):
#         subject_name = item.text()
#         self.current_subject = subject_name
#         self.file_paths = self.collect_nifti_files_for_subject(subject_name)
#         self.current_file_idx = 0
#         self.load_next_image()

#     def populate_subject_list(self):
#         subjects = set()
#         for file_path in self.file_paths:
#             subject_name = self.get_subject_name(file_path)
#             subjects.add(subject_name)
#         self.subject_list.addItems(sorted(subjects))

# def main():
#     root = tk.Tk()
#     root.withdraw()
#     directory = filedialog.askdirectory(title="Select Root Directory")
#     if directory:
#         app = QtWidgets.QApplication([])
#         validator = MRISegmentValidator(directory)
#         validator.show()
#         app.exec_()
#     else:
#         messagebox.showerror("Error", "No directory selected")

# if __name__ == "__main__":
#     main()

import os
import nibabel as nib
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets
import tkinter as tk
from tkinter import filedialog, messagebox

class MRISegmentValidator(QtWidgets.QWidget):
    def __init__(self, root_dir, segment_folder='3_segment'):
        super().__init__()
        self.root_dir = root_dir
        self.segment_folder = segment_folder
        self.current_image_type = "rc1"
        self.current_subject = None
        self.file_paths = self.collect_nifti_files()
        self.current_file_idx = 0
        self.segment_validations = {}
        self.processed_subjects = set()
        self.init_ui()
        self.load_next_image()

    def init_ui(self):
        self.setWindowTitle('MRI Segment Validator')
        self.resize(1200, 800)  # Set the default window size

        layout = QtWidgets.QVBoxLayout()
        top_layout = QtWidgets.QHBoxLayout()

        # Add radio buttons for rc1, rc2, and rc3
        self.rc1_radio = QtWidgets.QRadioButton('rc1')
        self.rc2_radio = QtWidgets.QRadioButton('rc2')
        self.rc3_radio = QtWidgets.QRadioButton('rc3')

        # Group the radio buttons together
        self.image_type_group = QtWidgets.QButtonGroup()
        self.image_type_group.addButton(self.rc1_radio)
        self.image_type_group.addButton(self.rc2_radio)
        self.image_type_group.addButton(self.rc3_radio)

        # Set rc1 as the default selected option
        self.rc1_radio.setChecked(True)

        self.image_type_group.buttonClicked.connect(self.on_image_type_changed)

        top_layout.addWidget(self.rc1_radio)
        top_layout.addWidget(self.rc2_radio)
        top_layout.addWidget(self.rc3_radio)

        layout.addLayout(top_layout)

        # Add subject name and image type display
        self.subject_name_label = QtWidgets.QLabel("Subject Name: ")
        self.subject_name_label.setFixedHeight(20)  # Adjust height
        layout.addWidget(self.subject_name_label)
        self.image_type_label = QtWidgets.QLabel("Image Type: ")
        self.image_type_label.setFixedHeight(20)  # Adjust height
        layout.addWidget(self.image_type_label)

        main_layout = QtWidgets.QHBoxLayout()

        # Add subject list
        self.subject_list = QtWidgets.QListWidget()
        self.subject_list.setFixedWidth(200)  # Adjust width
        self.subject_list.itemClicked.connect(self.on_subject_selected)
        main_layout.addWidget(self.subject_list)

        # Create layout for image views
        img_layout = QtWidgets.QVBoxLayout()
        self.view_coronal = pg.ImageView()
        self.view_axial = pg.ImageView()

        # Remove the scroll bars
        self.view_coronal.ui.histogram.hide()
        self.view_coronal.ui.roiBtn.hide()
        self.view_coronal.ui.menuBtn.hide()

        self.view_axial.ui.histogram.hide()
        self.view_axial.ui.roiBtn.hide()
        self.view_axial.ui.menuBtn.hide()

        img_layout.addWidget(self.view_coronal)
        img_layout.addWidget(self.view_axial)

        main_layout.addLayout(img_layout)
        layout.addLayout(main_layout)

        # Add sliders
        self.slider_coronal = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider_axial = QtWidgets.QSlider(QtCore.Qt.Horizontal)

        layout.addWidget(self.slider_coronal)
        layout.addWidget(self.slider_axial)

        self.valid_button = QtWidgets.QPushButton('Valid')
        self.invalid_button = QtWidgets.QPushButton('Invalid')

        self.valid_button.clicked.connect(lambda: self.validate_segmentation(True))
        self.invalid_button.clicked.connect(lambda: self.validate_segmentation(False))

        layout.addWidget(self.valid_button)
        layout.addWidget(self.invalid_button)

        # Checkbox for switching segment folders
        self.segment_checkbox = QtWidgets.QCheckBox("Switch to 2_segment")
        self.segment_checkbox.toggled.connect(self.switch_segment_folder)
        layout.addWidget(self.segment_checkbox)

        self.setLayout(layout)

        self.slider_coronal.valueChanged.connect(lambda val: self.on_scroll(val, 0))
        self.slider_axial.valueChanged.connect(lambda val: self.on_scroll(val, 1))

        self.populate_subject_list()

    def collect_nifti_files(self):
        file_paths = []
        for subject in sorted(os.listdir(self.root_dir)):
            subject_dir = os.path.join(self.root_dir, subject, 'segmentation', self.segment_folder, 'dartel_input_images')
            if os.path.isdir(subject_dir):
                rc_files = [os.path.join(subject_dir, f) for f in sorted(os.listdir(subject_dir)) if f.startswith('rc')]
                file_paths.extend(rc_files)
        return file_paths

    def load_image(self, file_path):
        img = nib.load(file_path)
        data = img.get_fdata()
        return data

    def load_next_image(self):
        if self.current_file_idx >= len(self.file_paths):
            messagebox.showinfo("Info", "Validation completed")
            self.save_results()
            self.close()
            return
        while self.current_file_idx < len(self.file_paths):
            file_path = self.file_paths[self.current_file_idx]
            if self.current_image_type not in file_path:
                self.current_file_idx += 1
                continue
            subject_name = self.get_subject_name(file_path)
            if subject_name in self.processed_subjects:
                self.current_file_idx += 1
            else:
                self.img_data = self.load_image(file_path)
                self.slice_indices = [self.img_data.shape[0] // 2, self.img_data.shape[1] // 2]
                self.update_sliders()
                self.display_image()
                self.update_labels()
                break

    def display_image(self):
        coronal_slice = np.rot90(self.img_data[self.slice_indices[0], :, :])
        axial_slice = np.rot90(self.img_data[:, self.slice_indices[1], :])

        self.view_coronal.setImage(coronal_slice)
        self.view_axial.setImage(axial_slice)

    def update_labels(self):
        subject_name = self.get_subject_name(self.file_paths[self.current_file_idx])
        self.subject_name_label.setText(f"Subject Name: {subject_name}")
        self.image_type_label.setText(f"Image Type: {self.current_image_type}")

    def get_subject_name(self, file_path):
        parts = file_path.split(os.sep)
        for i, part in enumerate(parts):
            if part == 'segmentation':
                return parts[i-1]
        return "Unknown Subject"

    def on_scroll(self, val, axis):
        self.slice_indices[axis] = int(val)
        self.display_image()

    def validate_segmentation(self, label):
        subject_name = self.get_subject_name(self.file_paths[self.current_file_idx])
        if not label:
            # If any image is invalid, mark all images for this subject as invalid
            for file_path in self.file_paths:
                if subject_name in file_path:
                    self.segment_validations[file_path] = False
                    self.processed_subjects.add(subject_name)
        else:
            # If marked as valid, only mark this specific image as valid
            self.segment_validations[self.file_paths[self.current_file_idx]] = True

        # Move to the next image
        self.current_file_idx += 1
        self.load_next_image()

    def save_results(self):
        with open(os.path.join(self.root_dir, 'validation_results.txt'), 'w') as f:
            for file, result in self.segment_validations.items():
                f.write(f"{file}: {'Valid' if result else 'Invalid'}\n")

    def update_sliders(self):
        self.slider_coronal.setMaximum(self.img_data.shape[0] - 1)
        self.slider_axial.setMaximum(self.img_data.shape[1] - 1)

        self.slider_coronal.setValue(self.slice_indices[0])
        self.slider_axial.setValue(self.slice_indices[1])

    def switch_segment_folder(self):
        if self.segment_checkbox.isChecked():
            self.segment_folder = '2_segment'
        else:
            self.segment_folder = '3_segment'
        self.file_paths = self.collect_nifti_files()
        self.current_file_idx = 0
        self.load_next_image()

    def set_image_type(self, image_type):
        self.current_image_type = image_type
        if self.current_subject:
            self.file_paths = self.collect_nifti_files_for_subject(self.current_subject)
        self.current_file_idx = 0
        self.load_next_image()

    def collect_nifti_files_for_subject(self, subject_name):
        file_paths = []
        subject_dir = os.path.join(self.root_dir, subject_name, 'segmentation', self.segment_folder, 'dartel_input_images')
        if os.path.isdir(subject_dir):
            rc_files = [os.path.join(subject_dir, f) for f in sorted(os.listdir(subject_dir)) if f.startswith('rc')]
            file_paths.extend(rc_files)
        return file_paths

    def on_image_type_changed(self, button):
        self.set_image_type(button.text())

    def on_subject_selected(self, item):
        subject_name = item.text()
        self.current_subject = subject_name
        self.file_paths = self.collect_nifti_files_for_subject(subject_name)
        self.current_file_idx = 0
        self.load_next_image()

    def populate_subject_list(self):
        subjects = set()
        for file_path in self.file_paths:
            subject_name = self.get_subject_name(file_path)
            subjects.add(subject_name)
        self.subject_list.addItems(sorted(subjects))

def main():
    root = tk.Tk()
    root.withdraw()
    directory = filedialog.askdirectory(title="Select Root Directory")
    if directory:
        app = QtWidgets.QApplication([])
        validator = MRISegmentValidator(directory)
        validator.show()
        app.exec_()
    else:
        messagebox.showerror("Error", "No directory selected")

if __name__ == "__main__":
    main()
