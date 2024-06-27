from modalities.segmentation_1 import segment_brain_images

output_files = segment_brain_images('data/alignment/', 'data/TPM/')
print(output_files)
