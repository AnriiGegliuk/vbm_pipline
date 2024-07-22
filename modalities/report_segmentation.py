import os
import nibabel as nb
import numpy as np
import matplotlib.pyplot as plt
import base64
from io import BytesIO

def plot_and_encode_image(image_data, slice_indices, orientation):
    """Plot multiple slices of the image and return the encoded image strings."""
    encoded_images = []
    for slice_index in slice_indices:
        if orientation == 'horizontal':
            slice_data = np.rot90(image_data[:, :, slice_index], 2)
        elif orientation == 'sagittal':
            slice_data = np.rot90(image_data[slice_index, :, :], 2)
        elif orientation == 'coronal':
            slice_data = np.rot90(image_data[:, slice_index, :], 2)
        plt.imshow(slice_data.T, cmap='gray', origin='lower')
        plt.axis('off')
        buf = BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        img_str = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()
        encoded_images.append(img_str)
    return encoded_images

def generate_html_report(report_data, output_dir):
    """Generate a general HTML report for all subjects."""
    html_content = """
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; }
            h1, h2, h3 { text-align: center; }
            .subject-section { margin-bottom: 40px; }
            .image-table { width: 100%; border-collapse: collapse; }
            .image-table, .image-table th, .image-table td { border: 1px solid black; }
            .image-table th, .image-table td { padding: 8px; text-align: center; }
            .image-table img { max-width: 200px; }
        </style>
    </head>
    <body>
    <h1>General Report for All Subjects</h1>
    """

    for data in report_data:
        subject_id = data['subject_id']
        html_content += f"<div class='subject-section'><h2>Subject {subject_id}</h2>"

        images = data['images']
        html_content += """
        <table class='image-table'>
            <tr>
                <th>Type</th>
                <th>Horizontal Slice</th>
                <th>Sagittal Slice</th>
                <th>Coronal Slice</th>
            </tr>
        """

        for img_type, img_dict in images['seg_images'].items():
            html_content += f"""
            <tr>
                <td>{img_type} Segmentation</td>
                <td><img src="data:image/png;base64,{img_dict['horizontal']}" /></td>
                <td><img src="data:image/png;base64,{img_dict['sagittal']}" /></td>
                <td><img src="data:image/png;base64,{img_dict['coronal']}" /></td>
            </tr>
            """
        
        html_content += f"""
        <tr>
            <td>Mask</td>
            <td><img src="data:image/png;base64,{images['mask_image']['horizontal']}" /></td>
            <td><img src="data:image/png;base64,{images['mask_image']['sagittal']}" /></td>
            <td><img src="data:image/png;base64,{images['mask_image']['coronal']}" /></td>
        </tr>
        </table></div>
        """

    html_content += "</body></html>"

    report_path = os.path.join(output_dir, 'general_report.html')
    with open(report_path, 'w') as f:
        f.write(html_content)

    return report_path

def process_subject(segmentation_dir, subject_id):
    images = {'seg_images': {}, 'mask_image': {}}

    # Load one of the images to get its shape
    img_path = os.path.join(segmentation_dir, 'native_class_images', f'c1{subject_id}.nii')
    img_nifti = nb.load(img_path)
    img_data = img_nifti.get_fdata()

    slice_indices = {
        'horizontal': img_data.shape[2] // 2,
        'sagittal': img_data.shape[0] // 2,
        'coronal': img_data.shape[1] // 2
    }

    for img_type in ['c1', 'c2', 'c3']:
        img_path = os.path.join(segmentation_dir, 'native_class_images', f'{img_type}{subject_id}.nii')
        img_nifti = nb.load(img_path)
        img_data = img_nifti.get_fdata()
        images['seg_images'][img_type] = {
            'horizontal': plot_and_encode_image(img_data, [slice_indices['horizontal']], 'horizontal')[0],
            'sagittal': plot_and_encode_image(img_data, [slice_indices['sagittal']], 'sagittal')[0],
            'coronal': plot_and_encode_image(img_data, [slice_indices['coronal']], 'coronal')[0]
        }

    mask_path = os.path.join(os.path.dirname(segmentation_dir), '3_mask', f'mask_{subject_id}.nii')
    mask_nifti = nb.load(mask_path)
    mask_data = mask_nifti.get_fdata()
    images['mask_image'] = {
        'horizontal': plot_and_encode_image(mask_data, [slice_indices['horizontal']], 'horizontal')[0],
        'sagittal': plot_and_encode_image(mask_data, [slice_indices['sagittal']], 'sagittal')[0],
        'coronal': plot_and_encode_image(mask_data, [slice_indices['coronal']], 'coronal')[0]
    }

    return {'subject_id': subject_id, 'images': images}

def traverse_and_generate_report(base_dir, output_dir):
    report_data = []

    for root, dirs, files in os.walk(base_dir):
        for dir_name in dirs:
            if dir_name == '3_segment':
                segmentation_dir = os.path.join(root, dir_name)
                subject_id = os.path.basename(os.path.dirname(os.path.dirname(segmentation_dir)))
                subject_report_data = process_subject(segmentation_dir, subject_id)
                report_data.append(subject_report_data)

    report_path = generate_html_report(report_data, output_dir)
    print(f'General report saved at: {report_path}')
