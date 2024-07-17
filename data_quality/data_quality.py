

# tested with dropdown menu

# import os
# import nibabel as nib
# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.widgets import Slider, Button, RadioButtons, AxesWidget
# import matplotlib.cbook as cbook
# import tkinter as tk
# from tkinter import filedialog, messagebox

# class Dropdown(AxesWidget):
#     def __init__(self, ax, labels, active=0):
#         super().__init__(ax)
#         self.labels = labels
#         self.active = active
#         self.label = ax.text(0.5, 0.5, labels[active], 
#                              horizontalalignment='center', 
#                              verticalalignment='center', 
#                              transform=ax.transAxes)
#         self.rect = ax.patch
#         self.rect.set_facecolor('lightgoldenrodyellow')
#         self.cids = [self.connect_event('button_press_event', self.on_click)]
#         self.menu = None
#         self._callbacks = cbook.CallbackRegistry()

#     def on_click(self, event):
#         if event.inaxes != self.ax:
#             return
#         if self.menu is None:
#             self.open_menu()
#         else:
#             self.close_menu()

#     def open_menu(self):
#         self.menu = plt.figure(figsize=(2, len(self.labels) * 0.25))
#         for i, label in enumerate(self.labels):
#             ax = self.menu.add_subplot(len(self.labels), 1, i + 1)
#             ax.text(0.5, 0.5, label, horizontalalignment='center', 
#                     verticalalignment='center', transform=ax.transAxes)
#             ax.set_axis_off()
#             ax.set_picker(True)
#             ax.label = label
#         self.menu.canvas.mpl_connect('pick_event', self.on_pick)

#     def on_pick(self, event):
#         self.active = self.labels.index(event.artist.label)
#         self.label.set_text(self.labels[self.active])
#         self.close_menu()
#         self._callbacks.process('selected', self.labels[self.active])

#     def close_menu(self):
#         plt.close(self.menu)
#         self.menu = None

#     def on_selected(self, func):
#         self._callbacks.connect('selected', func)

# class MRISegmentValidator:
#     def __init__(self, root_dir, segment_folder='3_segment'):
#         self.root_dir = root_dir
#         self.segment_folder = segment_folder
#         self.subjects = self.get_subjects()
#         self.current_subject = self.subjects[0]
#         self.file_paths = self.collect_nifti_files()
#         self.current_file_idx = 0
#         self.segment_validations = {}
#         self.fig, self.ax = plt.subplots(1, 3, figsize=(18, 6))
#         self.slice_indices = [0, 0, 0]
#         self.sliders = None
#         self.create_dropdown()
#         self.load_next_image()

#     def get_subjects(self):
#         subjects = [d for d in sorted(os.listdir(self.root_dir)) if os.path.isdir(os.path.join(self.root_dir, d))]
#         return subjects

#     def collect_nifti_files(self):
#         file_paths = []
#         subject_dir = os.path.join(self.root_dir, self.current_subject, 'segmentation', self.segment_folder, 'dartel_input_images')
#         if os.path.isdir(subject_dir):
#             rc_files = [os.path.join(subject_dir, f) for f in sorted(os.listdir(subject_dir)) if f.startswith('rc')]
#             file_paths.extend(rc_files)
#         return file_paths

#     def load_image(self, file_path):
#         img = nib.load(file_path)
#         data = img.get_fdata()
#         return data

#     def load_next_image(self):
#         if self.current_file_idx >= len(self.file_paths):
#             messagebox.showinfo("Info", "Validation completed")
#             self.save_results()
#             plt.close()
#             return
#         self.img_data = self.load_image(self.file_paths[self.current_file_idx])
#         self.slice_indices = [self.img_data.shape[0] // 2, self.img_data.shape[1] // 2, self.img_data.shape[2] // 2]
#         if self.sliders is None:
#             self.create_sliders()
#         self.update_sliders()
#         self.display_image()

#     def display_image(self):
#         for a in self.ax:
#             a.clear()
#         self.ax[0].imshow(np.rot90(self.img_data[:, self.slice_indices[1], :], 2), cmap='gray', origin='lower')
#         self.ax[1].imshow(np.rot90(self.img_data[self.slice_indices[0], :, :], 2), cmap='gray', origin='lower')
#         self.ax[2].imshow(np.rot90(self.img_data[:, :, self.slice_indices[2]], 1), cmap='gray', origin='lower')
#         self.ax[0].set_title('Axial Slice')
#         self.ax[1].set_title('Coronal Slice')
#         self.ax[2].set_title('Sagittal Slice')
#         for a in self.ax:
#             a.axis('off')
#         subject_name = self.current_subject
#         self.fig.suptitle(subject_name, fontsize=16)
#         plt.draw()

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
#         self.segment_validations[self.file_paths[self.current_file_idx]] = label
#         self.current_file_idx += 1
#         self.load_next_image()

#     def save_results(self):
#         with open(os.path.join(self.root_dir, 'validation_results.txt'), 'w') as f:
#             for file, result in self.segment_validations.items():
#                 f.write(f"{file}: {'Valid' if result else 'Invalid'}\n")

#     def create_sliders(self):
#         axcolor = 'lightgoldenrodyellow'
#         self.slider_axs = [
#             self.fig.add_axes([0.15, 0.01, 0.65, 0.03], facecolor=axcolor),
#             self.fig.add_axes([0.15, 0.04, 0.65, 0.03], facecolor=axcolor),
#             self.fig.add_axes([0.15, 0.07, 0.65, 0.03], facecolor=axcolor),
#         ]
#         self.sliders = [
#             Slider(self.slider_axs[2], 'Axial Slice', 0, self.img_data.shape[2] - 1, valinit=self.slice_indices[2], valfmt='%0.0f'),
#             Slider(self.slider_axs[1], 'Coronal Slice', 0, self.img_data.shape[0] - 1, valinit=self.slice_indices[0], valfmt='%0.0f'),
#             Slider(self.slider_axs[0], 'Sagittal Slice', 0, self.img_data.shape[1] - 1, valinit=self.slice_indices[1], valfmt='%0.0f'),
#         ]
#         self.sliders[0].on_changed(lambda val: self.on_scroll(val, 1))
#         self.sliders[1].on_changed(lambda val: self.on_scroll(val, 0))
#         self.sliders[2].on_changed(lambda val: self.on_scroll(val, 2))

#     def update_sliders(self):
#         self.sliders[0].valmax = self.img_data.shape[1] - 1
#         self.sliders[1].valmax = self.img_data.shape[0] - 1
#         self.sliders[2].valmax = self.img_data.shape[2] - 1
#         self.sliders[0].set_val(self.slice_indices[1])
#         self.sliders[1].set_val(self.slice_indices[0])
#         self.sliders[2].set_val(self.slice_indices[2])

#     def create_dropdown(self):
#         dropdown_ax = self.fig.add_axes([0.3, 0.9, 0.4, 0.05])
#         self.dropdown = Dropdown(dropdown_ax, self.subjects)
#         self.dropdown.on_selected(self.on_subject_select)

#     def on_subject_select(self, subject):
#         self.current_subject = subject
#         self.file_paths = self.collect_nifti_files()
#         self.current_file_idx = 0
#         self.load_next_image()

#     def run(self):
#         valid_button_ax = self.fig.add_axes([0.7, 0.9, 0.1, 0.075])
#         valid_button = Button(valid_button_ax, 'Valid')
#         valid_button.on_clicked(lambda event: self.validate_segmentation(True))

#         invalid_button_ax = self.fig.add_axes([0.81, 0.9, 0.1, 0.075])
#         invalid_button = Button(invalid_button_ax, 'Invalid')
#         invalid_button.on_clicked(lambda event: self.validate_segmentation(False))

#         radio_ax = self.fig.add_axes([0.01, 0.4, 0.1, 0.15], facecolor='lightgoldenrodyellow')
#         radio = RadioButtons(radio_ax, ('3_segment', '2_segment'))
#         radio.on_clicked(self.switch_segment_folder)

#         plt.subplots_adjust(left=0.1, bottom=0.15, right=0.9, top=0.85)
#         plt.show()

#     def switch_segment_folder(self, label):
#         self.segment_folder = label
#         self.file_paths = self.collect_nifti_files()
#         self.current_file_idx = 0
#         self.load_next_image()

# def main():
#     root = tk.Tk()
#     root.withdraw()
#     directory = filedialog.askdirectory(title="Select Root Directory")
#     if directory:
#         validator = MRISegmentValidator(directory)
#         validator.run()
#     else:
#         messagebox.showerror("Error", "No directory selected")

# if __name__ == "__main__":
#     main()







### was final we


import os
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
import tkinter as tk
from tkinter import filedialog, messagebox

class MRISegmentValidator:
    def __init__(self, root_dir, segment_folder='3_segment'):
        self.root_dir = root_dir
        self.segment_folder = segment_folder
        self.file_paths = self.collect_nifti_files()
        self.current_file_idx = 0
        self.segment_validations = {}
        self.fig, self.ax = plt.subplots(1, 3, figsize=(18, 6))
        self.slice_indices = [0, 0, 0]
        self.sliders = None
        self.load_next_image()

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
            plt.close()
            return
        self.img_data = self.load_image(self.file_paths[self.current_file_idx])
        self.slice_indices = [self.img_data.shape[0] // 2, self.img_data.shape[1] // 2, self.img_data.shape[2] // 2]
        if self.sliders is None:
            self.create_sliders()
        self.update_sliders()
        self.display_image()

    def display_image(self):
        for a in self.ax:
            a.clear()
        self.ax[0].imshow(np.rot90(self.img_data[:, self.slice_indices[1], :], 2), cmap='gray', origin='lower')
        self.ax[1].imshow(np.rot90(self.img_data[self.slice_indices[0], :, :], 2), cmap='gray', origin='lower')
        self.ax[2].imshow(np.rot90(self.img_data[:, :, self.slice_indices[2]], ), cmap='gray', origin='lower')
        self.ax[0].set_title('Axial Slice')
        self.ax[1].set_title('Coronal Slice')
        self.ax[2].set_title('Sagittal Slice')
        for a in self.ax:
            a.axis('off')
        subject_name = self.get_subject_name(self.file_paths[self.current_file_idx])
        self.fig.suptitle(subject_name, fontsize=16)
        plt.draw()

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
        self.segment_validations[self.file_paths[self.current_file_idx]] = label
        self.current_file_idx += 1
        self.load_next_image()

    def save_results(self):
        with open(os.path.join(self.root_dir, 'validation_results.txt'), 'w') as f:
            for file, result in self.segment_validations.items():
                f.write(f"{file}: {'Valid' if result else 'Invalid'}\n")

    def create_sliders(self):
        axcolor = 'lightgoldenrodyellow'
        self.slider_axs = [
            self.fig.add_axes([0.15, 0.01, 0.65, 0.03], facecolor=axcolor),
            self.fig.add_axes([0.15, 0.04, 0.65, 0.03], facecolor=axcolor),
            self.fig.add_axes([0.15, 0.07, 0.65, 0.03], facecolor=axcolor),
        ]
        self.sliders = [
            Slider(self.slider_axs[2], 'Axial Slice', 0, self.img_data.shape[2] - 1, valinit=self.slice_indices[2], valfmt='%0.0f'),
            Slider(self.slider_axs[1], 'Coronal Slice', 0, self.img_data.shape[0] - 1, valinit=self.slice_indices[0], valfmt='%0.0f'),
            Slider(self.slider_axs[0], 'Sagittal Slice', 0, self.img_data.shape[1] - 1, valinit=self.slice_indices[1], valfmt='%0.0f'),
        ]
        self.sliders[0].on_changed(lambda val: self.on_scroll(val, 1))
        self.sliders[1].on_changed(lambda val: self.on_scroll(val, 0))
        self.sliders[2].on_changed(lambda val: self.on_scroll(val, 2))

    def update_sliders(self):
        self.sliders[0].valmax = self.img_data.shape[1] - 1
        self.sliders[1].valmax = self.img_data.shape[0] - 1
        self.sliders[2].valmax = self.img_data.shape[2] - 1
        self.sliders[0].set_val(self.slice_indices[1])
        self.sliders[1].set_val(self.slice_indices[0])
        self.sliders[2].set_val(self.slice_indices[2])

    def run(self):
        valid_button_ax = self.fig.add_axes([0.7, 0.9, 0.1, 0.075])
        valid_button = Button(valid_button_ax, 'Valid')
        valid_button.on_clicked(lambda event: self.validate_segmentation(True))

        invalid_button_ax = self.fig.add_axes([0.81, 0.9, 0.1, 0.075])
        invalid_button = Button(invalid_button_ax, 'Invalid')
        invalid_button.on_clicked(lambda event: self.validate_segmentation(False))

        radio_ax = self.fig.add_axes([0.01, 0.4, 0.1, 0.15], facecolor='lightgoldenrodyellow')
        radio = RadioButtons(radio_ax, ('3_segment', '2_segment'))
        radio.on_clicked(self.switch_segment_folder)

        plt.subplots_adjust(left=0.1, bottom=0.15, right=0.9, top=0.85)
        plt.show()

    def switch_segment_folder(self, label):
        self.segment_folder = label
        self.file_paths = self.collect_nifti_files()
        self.current_file_idx = 0
        self.load_next_image()

def main():
    root = tk.Tk()
    root.withdraw()
    directory = filedialog.askdirectory(title="Select Root Directory")
    if directory:
        validator = MRISegmentValidator(directory)
        validator.run()
    else:
        messagebox.showerror("Error", "No directory selected")

if __name__ == "__main__":
    main()










####### works as expected

# import os
# import nibabel as nib
# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.widgets import Slider, Button, RadioButtons
# import tkinter as tk
# from tkinter import filedialog, messagebox

# class MRISegmentValidator:
#     def __init__(self, root_dir, segment_folder='3_segment'):
#         self.root_dir = root_dir
#         self.segment_folder = segment_folder
#         self.file_paths = self.collect_nifti_files()
#         self.current_file_idx = 0
#         self.segment_validations = {}
#         self.fig, self.ax = plt.subplots(1, 3, figsize=(18, 6))
#         self.slice_indices = [0, 0, 0]
#         self.sliders = None
#         self.load_next_image()

#     def collect_nifti_files(self):
#         file_paths = []
#         for root, dirs, files in os.walk(self.root_dir):
#             for file in files:
#                 if file.endswith('.nii') and self.segment_folder in root and 'dartel_input_images' in root:
#                     file_paths.append(os.path.join(root, file))
#         return file_paths

#     def load_image(self, file_path):
#         img = nib.load(file_path)
#         data = img.get_fdata()  # Flip the image to correct orientation
#         return data

#     def load_next_image(self):
#         if self.current_file_idx >= len(self.file_paths):
#             messagebox.showinfo("Info", "Validation completed")
#             self.save_results()
#             plt.close()
#             return
#         self.img_data = self.load_image(self.file_paths[self.current_file_idx])
#         self.slice_indices = [self.img_data.shape[0] // 2, self.img_data.shape[1] // 2, self.img_data.shape[2] // 2]
#         if self.sliders is None:
#             self.create_sliders()
#         self.update_sliders()
#         self.display_image()

#     def display_image(self):
#         for a in self.ax:
#             a.clear()
#         self.ax[0].imshow(self.img_data[:, self.slice_indices[1], :], cmap='gray')
#         self.ax[1].imshow(self.img_data[self.slice_indices[0], :, :], cmap='gray')
#         self.ax[2].imshow(np.rot90(self.img_data[:, :, self.slice_indices[2]], 3), cmap='gray')
#         self.ax[0].set_title('Axial Slice')
#         self.ax[1].set_title('Coronal Slice')
#         self.ax[2].set_title('Sagittal Slice')
#         for a in self.ax:
#             a.axis('off')
#         subject_name = self.get_subject_name(self.file_paths[self.current_file_idx])
#         self.fig.suptitle(subject_name, fontsize=16)
#         plt.draw()

#     def get_subject_name(self, file_path):
#         parts = file_path.split(os.sep)
#         for part in parts:
#             if part.startswith('T2_'):
#                 return part
#         return "Unknown Subject"

#     def on_scroll(self, val, axis):
#         self.slice_indices[axis] = int(val)
#         self.display_image()

#     def validate_segmentation(self, label):
#         self.segment_validations[self.file_paths[self.current_file_idx]] = label
#         self.current_file_idx += 1
#         self.load_next_image()

#     def save_results(self):
#         with open(os.path.join(self.root_dir, 'validation_results.txt'), 'w') as f:
#             for file, result in self.segment_validations.items():
#                 f.write(f"{file}: {'Valid' if result else 'Invalid'}\n")

#     def create_sliders(self):
#         axcolor = 'lightgoldenrodyellow'
#         self.slider_axs = [
#             self.fig.add_axes([0.15, 0.01, 0.65, 0.03], facecolor=axcolor),
#             self.fig.add_axes([0.15, 0.04, 0.65, 0.03], facecolor=axcolor),
#             self.fig.add_axes([0.15, 0.07, 0.65, 0.03], facecolor=axcolor),
#         ]
#         self.sliders = [
#             Slider(self.slider_axs[2], 'Axial Slice', 0, self.img_data.shape[2] - 1, valinit=self.slice_indices[2], valfmt='%0.0f'),
#             Slider(self.slider_axs[1], 'Coronal Slice', 0, self.img_data.shape[0] - 1, valinit=self.slice_indices[0], valfmt='%0.0f'),
#             Slider(self.slider_axs[0], 'Sarigal Slice', 0, self.img_data.shape[1] - 1, valinit=self.slice_indices[1], valfmt='%0.0f'),
#         ]
#         self.sliders[0].on_changed(lambda val: self.on_scroll(val, 1))
#         self.sliders[1].on_changed(lambda val: self.on_scroll(val, 0))
#         self.sliders[2].on_changed(lambda val: self.on_scroll(val, 2))

#     def update_sliders(self):
#         self.sliders[0].valmax = self.img_data.shape[1] - 1
#         self.sliders[1].valmax = self.img_data.shape[0] - 1
#         self.sliders[2].valmax = self.img_data.shape[2] - 1
#         self.sliders[0].set_val(self.slice_indices[1])
#         self.sliders[1].set_val(self.slice_indices[0])
#         self.sliders[2].set_val(self.slice_indices[2])

#     def run(self):
#         valid_button_ax = self.fig.add_axes([0.7, 0.9, 0.1, 0.075])
#         valid_button = Button(valid_button_ax, 'Valid')
#         valid_button.on_clicked(lambda event: self.validate_segmentation(True))

#         invalid_button_ax = self.fig.add_axes([0.81, 0.9, 0.1, 0.075])
#         invalid_button = Button(invalid_button_ax, 'Invalid')
#         invalid_button.on_clicked(lambda event: self.validate_segmentation(False))

#         radio_ax = self.fig.add_axes([0.01, 0.4, 0.1, 0.15], facecolor='lightgoldenrodyellow')
#         radio = RadioButtons(radio_ax, ('3_segment', '2_segment'))
#         radio.on_clicked(self.switch_segment_folder)

#         plt.subplots_adjust(left=0.1, bottom=0.15, right=0.9, top=0.85)
#         plt.show()

#     def switch_segment_folder(self, label):
#         self.segment_folder = label
#         self.file_paths = self.collect_nifti_files()
#         self.current_file_idx = 0
#         self.load_next_image()

# def main():
#     root = tk.Tk()
#     root.withdraw()
#     directory = filedialog.askdirectory(title="Select Root Directory")
#     if directory:
#         validator = MRISegmentValidator(directory)
#         validator.run()
#     else:
#         messagebox.showerror("Error", "No directory selected")

# if __name__ == "__main__":
#     main()












# import os
# import nibabel as nib
# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.widgets import Slider, Button
# import tkinter as tk
# from tkinter import filedialog, messagebox

# class MRISegmentValidator:
#     def __init__(self, root_dir):
#         self.root_dir = root_dir
#         self.file_paths = self.collect_nifti_files()
#         self.current_file_idx = 0
#         self.segment_validations = {}
#         self.fig, self.ax = plt.subplots(1, 3, figsize=(18, 6))
#         self.slice_indices = [0, 0, 0]
#         self.sliders = None
#         self.load_next_image()

#     def collect_nifti_files(self):
#         file_paths = []
#         for root, dirs, files in os.walk(self.root_dir):
#             for file in files:
#                 if file.endswith('.nii') and 'dartel_input_images' in root:
#                     file_paths.append(os.path.join(root, file))
#         return file_paths

#     def load_image(self, file_path):
#         img = nib.load(file_path)
#         data = np.flipud(img.get_fdata())  # Flip the image to correct orientation
#         return data

#     def load_next_image(self):
#         if self.current_file_idx >= len(self.file_paths):
#             messagebox.showinfo("Info", "Validation completed")
#             self.save_results()
#             plt.close()
#             return
#         self.img_data = self.load_image(self.file_paths[self.current_file_idx])
#         self.slice_indices = [self.img_data.shape[0] // 2, self.img_data.shape[1] // 2, self.img_data.shape[2] // 2]
#         if self.sliders is None:
#             self.create_sliders()
#         self.update_sliders()
#         self.display_image()

#     def display_image(self):
#         for a in self.ax:
#             a.clear()
#         # self.ax[0].imshow(np.rot90(self.img_data[self.slice_indices[0], :, :]), cmap='gray')
#         self.ax[0].imshow(self.img_data[self.slice_indices[0], :, :], cmap='gray')
#         # self.ax[1].imshow(np.rot90(self.img_data[:, self.slice_indices[1], :]), cmap='gray')
#         self.ax[1].imshow(self.img_data[:, self.slice_indices[1], :], cmap='gray')
#         # self.ax[2].imshow(np.rot90(self.img_data[:, :, self.slice_indices[2]]), cmap='gray')
#         self.ax[2].imshow(self.img_data[:, :, self.slice_indices[2]], cmap='gray')
#         self.ax[0].set_title('Sagittal Slice')
#         self.ax[1].set_title('Coronal Slice')
#         self.ax[2].set_title('Axial Slice')
#         for a in self.ax:
#             a.axis('off')
#         plt.draw()

#     def on_scroll(self, val, axis):
#         self.slice_indices[axis] = int(val)
#         self.display_image()

#     def validate_segmentation(self, label):
#         self.segment_validations[self.file_paths[self.current_file_idx]] = label
#         self.current_file_idx += 1
#         self.load_next_image()

#     def save_results(self):
#         with open(os.path.join(self.root_dir, 'validation_results.txt'), 'w') as f:
#             for file, result in self.segment_validations.items():
#                 f.write(f"{file}: {'Valid' if result else 'Invalid'}\n")

#     def create_sliders(self):
#         axcolor = 'lightgoldenrodyellow'
#         self.slider_axs = [
#             self.fig.add_axes([0.15, 0.01, 0.65, 0.03], facecolor=axcolor),
#             self.fig.add_axes([0.15, 0.04, 0.65, 0.03], facecolor=axcolor),
#             self.fig.add_axes([0.15, 0.07, 0.65, 0.03], facecolor=axcolor),
#         ]
#         self.sliders = [
#             Slider(self.slider_axs[0], 'Sagittal', 0, self.img_data.shape[0] - 1, valinit=self.slice_indices[0], valfmt='%0.0f'),
#             Slider(self.slider_axs[1], 'Coronal', 0, self.img_data.shape[1] - 1, valinit=self.slice_indices[1], valfmt='%0.0f'),
#             Slider(self.slider_axs[2], 'Axial', 0, self.img_data.shape[2] - 1, valinit=self.slice_indices[2], valfmt='%0.0f'),
#         ]
#         self.sliders[0].on_changed(lambda val: self.on_scroll(val, 0))
#         self.sliders[1].on_changed(lambda val: self.on_scroll(val, 1))
#         self.sliders[2].on_changed(lambda val: self.on_scroll(val, 2))

#     def update_sliders(self):
#         self.sliders[0].valmax = self.img_data.shape[0] - 1
#         self.sliders[1].valmax = self.img_data.shape[1] - 1
#         self.sliders[2].valmax = self.img_data.shape[2] - 1
#         self.sliders[0].set_val(self.slice_indices[0])
#         self.sliders[1].set_val(self.slice_indices[1])
#         self.sliders[2].set_val(self.slice_indices[2])

#     def run(self):
#         valid_button_ax = self.fig.add_axes([0.7, 0.9, 0.1, 0.075])
#         valid_button = Button(valid_button_ax, 'Valid')
#         valid_button.on_clicked(lambda event: self.validate_segmentation(True))

#         invalid_button_ax = self.fig.add_axes([0.81, 0.9, 0.1, 0.075])
#         invalid_button = Button(invalid_button_ax, 'Invalid')
#         invalid_button.on_clicked(lambda event: self.validate_segmentation(False))

#         plt.subplots_adjust(left=0.1, bottom=0.15, right=0.9, top=0.85)
#         plt.show()

# def main():
#     root = tk.Tk()
#     root.withdraw()
#     directory = filedialog.askdirectory(title="Select Root Directory")
#     if directory:
#         validator = MRISegmentValidator(directory)
#         validator.run()
#     else:
#         messagebox.showerror("Error", "No directory selected")

# if __name__ == "__main__":
#     main()





# ### closer to what I want 

# # import os
# # import nibabel as nib
# # import numpy as np
# # import matplotlib.pyplot as plt
# # from matplotlib.widgets import Slider, Button
# # import tkinter as tk
# # from tkinter import filedialog, messagebox

# # class MRISegmentValidator:
# #     def __init__(self, root_dir):
# #         self.root_dir = root_dir
# #         self.file_paths = self.collect_nifti_files()
# #         self.current_file_idx = 0
# #         self.segment_validations = {}
# #         self.fig, self.ax = plt.subplots(1, 3)
# #         self.slice_indices = [0, 0, 0]
# #         self.sliders = None
# #         self.load_next_image()

# #     def collect_nifti_files(self):
# #         file_paths = []
# #         for root, dirs, files in os.walk(self.root_dir):
# #             for file in files:
# #                 if file.endswith('.nii') and 'dartel_input_images' in root:
# #                     file_paths.append(os.path.join(root, file))
# #         return file_paths

# #     def load_image(self, file_path):
# #         img = nib.load(file_path)
# #         data = np.flipud(img.get_fdata())  # Flip the image to correct orientation
# #         return data

# #     def load_next_image(self):
# #         if self.current_file_idx >= len(self.file_paths):
# #             messagebox.showinfo("Info", "Validation completed")
# #             self.save_results()
# #             plt.close()
# #             return
# #         self.img_data = self.load_image(self.file_paths[self.current_file_idx])
# #         self.slice_indices = [self.img_data.shape[0] // 2, self.img_data.shape[1] // 2, self.img_data.shape[2] // 2]
# #         if self.sliders is None:
# #             self.create_sliders()
# #         self.update_sliders()
# #         self.display_image()

# #     def display_image(self):
# #         self.ax[0].imshow(self.img_data[self.slice_indices[0], :, :], cmap='gray')
# #         self.ax[1].imshow(self.img_data[:, self.slice_indices[1], :], cmap='gray')
# #         self.ax[2].imshow(self.img_data[:, :, self.slice_indices[2]], cmap='gray')
# #         self.ax[0].set_title('Sagittal Slice')
# #         self.ax[1].set_title('Coronal Slice')
# #         self.ax[2].set_title('Horizontal Slice')
# #         plt.draw()

# #     def on_scroll(self, val, axis):
# #         self.slice_indices[axis] = int(val)
# #         self.display_image()

# #     def validate_segmentation(self, label):
# #         self.segment_validations[self.file_paths[self.current_file_idx]] = label
# #         self.current_file_idx += 1
# #         self.load_next_image()

# #     def save_results(self):
# #         with open(os.path.join(self.root_dir, 'validation_results.txt'), 'w') as f:
# #             for file, result in self.segment_validations.items():
# #                 f.write(f"{file}: {'Valid' if result else 'Invalid'}\n")

# #     def create_sliders(self):
# #         axcolor = 'lightgoldenrodyellow'
# #         self.slider_axs = [
# #             self.fig.add_axes([0.15, 0.01, 0.65, 0.03], facecolor=axcolor),
# #             self.fig.add_axes([0.15, 0.04, 0.65, 0.03], facecolor=axcolor),
# #             self.fig.add_axes([0.15, 0.07, 0.65, 0.03], facecolor=axcolor),
# #         ]
# #         self.sliders = [
# #             Slider(self.slider_axs[0], 'Sagittal', 0, self.img_data.shape[0] - 1, valinit=self.slice_indices[0], valfmt='%0.0f'),
# #             Slider(self.slider_axs[1], 'Coronal', 0, self.img_data.shape[1] - 1, valinit=self.slice_indices[1], valfmt='%0.0f'),
# #             Slider(self.slider_axs[2], 'Horizontal', 0, self.img_data.shape[2] - 1, valinit=self.slice_indices[2], valfmt='%0.0f'),
# #         ]
# #         self.sliders[0].on_changed(lambda val: self.on_scroll(val, 0))
# #         self.sliders[1].on_changed(lambda val: self.on_scroll(val, 1))
# #         self.sliders[2].on_changed(lambda val: self.on_scroll(val, 2))

# #     def update_sliders(self):
# #         self.sliders[0].valmax = self.img_data.shape[0] - 1
# #         self.sliders[1].valmax = self.img_data.shape[1] - 1
# #         self.sliders[2].valmax = self.img_data.shape[2] - 1
# #         self.sliders[0].set_val(self.slice_indices[0])
# #         self.sliders[1].set_val(self.slice_indices[1])
# #         self.sliders[2].set_val(self.slice_indices[2])

# #     def run(self):
# #         valid_button_ax = self.fig.add_axes([0.7, 0.9, 0.1, 0.075])
# #         valid_button = Button(valid_button_ax, 'Valid')
# #         valid_button.on_clicked(lambda event: self.validate_segmentation(True))

# #         invalid_button_ax = self.fig.add_axes([0.81, 0.9, 0.1, 0.075])
# #         invalid_button = Button(invalid_button_ax, 'Invalid')
# #         invalid_button.on_clicked(lambda event: self.validate_segmentation(False))

# #         plt.subplots_adjust(left=0.1, bottom=0.15, right=0.9, top=0.85)
# #         plt.show()

# # def main():
# #     root = tk.Tk()
# #     root.withdraw()
# #     directory = filedialog.askdirectory(title="Select Root Directory")
# #     if directory:
# #         validator = MRISegmentValidator(directory)
# #         validator.run()
# #     else:
# #         messagebox.showerror("Error", "No directory selected")

# # if __name__ == "__main__":
# #     main()








# # import os
# # import nibabel as nib
# # import matplotlib.pyplot as plt
# # from matplotlib.widgets import CheckButtons
# # import tkinter as tk
# # from tkinter import filedialog, messagebox

# # class MRISegmentValidator:
# #     def __init__(self, root_dir):
# #         self.root_dir = root_dir
# #         self.file_paths = self.collect_nifti_files()
# #         self.current_file_idx = 0
# #         self.segment_validations = {}
# #         self.fig, self.ax = plt.subplots()
# #         self.check = None

# #     def collect_nifti_files(self):
# #         file_paths = []
# #         for root, dirs, files in os.walk(self.root_dir):
# #             for file in files:
# #                 if file.endswith('.nii') and 'dartel_input_images' in root:
# #                     file_paths.append(os.path.join(root, file))
# #         return file_paths

# #     def load_image(self, file_path):
# #         img = nib.load(file_path)
# #         data = img.get_fdata()
# #         return data

# #     def display_image(self, data):
# #         self.ax.clear()
# #         self.ax.imshow(data[:, :, data.shape[2] // 2], cmap='gray')
# #         self.ax.set_title(os.path.basename(self.file_paths[self.current_file_idx]))
# #         plt.draw()

# #     def validate_segmentation(self, label):
# #         self.segment_validations[self.file_paths[self.current_file_idx]] = label
# #         self.next_image()

# #     def next_image(self):
# #         self.current_file_idx += 1
# #         if self.current_file_idx >= len(self.file_paths):
# #             messagebox.showinfo("Info", "Validation completed")
# #             self.save_results()
# #             plt.close()
# #             return
# #         img_data = self.load_image(self.file_paths[self.current_file_idx])
# #         self.display_image(img_data)

# #     def save_results(self):
# #         with open(os.path.join(self.root_dir, 'validation_results.txt'), 'w') as f:
# #             for file, result in self.segment_validations.items():
# #                 f.write(f"{file}: {'Valid' if result else 'Invalid'}\n")

# #     def run(self):
# #         self.fig.canvas.mpl_connect('key_press_event', self.on_key)
# #         img_data = self.load_image(self.file_paths[self.current_file_idx])
# #         self.display_image(img_data)
# #         plt.show()

# #     def on_key(self, event):
# #         if event.key == 'y':
# #             self.validate_segmentation(True)
# #         elif event.key == 'n':
# #             self.validate_segmentation(False)

# # def main():
# #     root = tk.Tk()
# #     root.withdraw()
# #     directory = filedialog.askdirectory(title="Select Root Directory")
# #     if directory:
# #         validator = MRISegmentValidator(directory)
# #         validator.run()
# #     else:
# #         messagebox.showerror("Error", "No directory selected")

# # if __name__ == "__main__":
# #     main()


# # import os
# # import nibabel as nib
# # import numpy as np
# # import matplotlib.pyplot as plt
# # from matplotlib.widgets import Button
# # import tkinter as tk
# # from tkinter import filedialog, messagebox

# # class MRISegmentValidator:
# #     def __init__(self, root_dir):
# #         self.root_dir = root_dir
# #         self.file_paths = self.collect_nifti_files()
# #         self.current_file_idx = 0
# #         self.segment_validations = {}
# #         self.fig, self.ax = plt.subplots(1, 3)
# #         self.slice_indices = [0, 0, 0]
# #         self.load_next_image()

# #     def collect_nifti_files(self):
# #         file_paths = []
# #         for root, dirs, files in os.walk(self.root_dir):
# #             for file in files:
# #                 if file.endswith('.nii') and 'dartel_input_images' in root:
# #                     file_paths.append(os.path.join(root, file))
# #         return file_paths

# #     def load_image(self, file_path):
# #         img = nib.load(file_path)
# #         data = np.rot90(img.get_fdata(), k=1, axes=(0, 1))  # Rotate image 90 degrees
# #         return data

# #     def load_next_image(self):
# #         if self.current_file_idx >= len(self.file_paths):
# #             messagebox.showinfo("Info", "Validation completed")
# #             self.save_results()
# #             plt.close()
# #             return
# #         self.img_data = self.load_image(self.file_paths[self.current_file_idx])
# #         self.slice_indices = [self.img_data.shape[0] // 2, self.img_data.shape[1] // 2, self.img_data.shape[2] // 2]
# #         self.display_image()

# #     def display_image(self):
# #         self.ax[0].imshow(self.img_data[self.slice_indices[0], :, :], cmap='gray')
# #         self.ax[1].imshow(self.img_data[:, self.slice_indices[1], :], cmap='gray')
# #         self.ax[2].imshow(self.img_data[:, :, self.slice_indices[2]], cmap='gray')
# #         self.ax[0].set_title('Sagittal Slice')
# #         self.ax[1].set_title('Coronal Slice')
# #         self.ax[2].set_title('Horizontal Slice')
# #         plt.draw()

# #     def on_scroll(self, event):
# #         if event.inaxes == self.ax[0]:
# #             self.slice_indices[0] = (self.slice_indices[0] + 1) % self.img_data.shape[0]
# #         elif event.inaxes == self.ax[1]:
# #             self.slice_indices[1] = (self.slice_indices[1] + 1) % self.img_data.shape[1]
# #         elif event.inaxes == self.ax[2]:
# #             self.slice_indices[2] = (self.slice_indices[2] + 1) % self.img_data.shape[2]
# #         self.display_image()

# #     def validate_segmentation(self, label):
# #         self.segment_validations[self.file_paths[self.current_file_idx]] = label
# #         self.current_file_idx += 1
# #         self.load_next_image()

# #     def save_results(self):
# #         with open(os.path.join(self.root_dir, 'validation_results.txt'), 'w') as f:
# #             for file, result in self.segment_validations.items():
# #                 f.write(f"{file}: {'Valid' if result else 'Invalid'}\n")

# #     def run(self):
# #         self.fig.canvas.mpl_connect('scroll_event', self.on_scroll)
# #         valid_button_ax = self.fig.add_axes([0.7, 0.05, 0.1, 0.075])
# #         valid_button = Button(valid_button_ax, 'Valid')
# #         valid_button.on_clicked(lambda event: self.validate_segmentation(True))

# #         invalid_button_ax = self.fig.add_axes([0.81, 0.05, 0.1, 0.075])
# #         invalid_button = Button(invalid_button_ax, 'Invalid')
# #         invalid_button.on_clicked(lambda event: self.validate_segmentation(False))

# #         plt.show()

# # def main():
# #     root = tk.Tk()
# #     root.withdraw()
# #     directory = filedialog.askdirectory(title="Select Root Directory")
# #     if directory:
# #         validator = MRISegmentValidator(directory)
# #         validator.run()
# #     else:
# #         messagebox.showerror("Error", "No directory selected")

# # if __name__ == "__main__":
# #     main()
