from PIL import Image
import matplotlib.pyplot as plt

# Load images in desired order
lab_1m = Image.open(r"Python_RIS\DANE_Z_POMIAROW\ComCom_IEEEAccess\heatmapy_inny_kolor\heatmapy\heatmap_pattern_2_dist_1m_METIS.jpg")
lab_1_5m = Image.open(r"Python_RIS\DANE_Z_POMIAROW\ComCom_IEEEAccess\heatmapy_inny_kolor\heatmapy\heatmap_pattern_2_dist_1.5m_METIS.jpg")
lab_2m = Image.open(r"Python_RIS\DANE_Z_POMIAROW\ComCom_IEEEAccess\heatmapy_inny_kolor\heatmapy\heatmap_pattern_2_dist_2m_METIS.jpg")

chamber_1m = Image.open(r"Python_RIS\DANE_Z_POMIAROW\ComCom_IEEEAccess\heatmapy_inny_kolor\heatmapy\heatmap_pattern_2_dist_1m_AINFO.jpg")
chamber_1_5m = Image.open(r"Python_RIS\DANE_Z_POMIAROW\ComCom_IEEEAccess\heatmapy_inny_kolor\heatmapy\heatmap_pattern_2_dist_1.5m_AINFO.jpg")
chamber_2m = Image.open(r"Python_RIS\DANE_Z_POMIAROW\ComCom_IEEEAccess\heatmapy_inny_kolor\heatmapy\heatmap_pattern_2_dist_2m_AINFO.jpg")

# Resize all images to the same size (assuming they're similar)
size = lab_1m.size
images_row1 = [img.resize(size) for img in [lab_1m, lab_1_5m, lab_2m]]
images_row2 = [img.resize(size) for img in [chamber_1m, chamber_1_5m, chamber_2m]]

# Combine images into rows
def combine_images_horizontally(images):
    total_width = sum(img.width for img in images)
    max_height = max(img.height for img in images)
    combined = Image.new("RGB", (total_width, max_height))
    x_offset = 0
    for img in images:
        combined.paste(img, (x_offset, 0))
        x_offset += img.width
    return combined

row1 = combine_images_horizontally(images_row1)
row2 = combine_images_horizontally(images_row2)

# Combine rows vertically
final_image = Image.new("RGB", (row1.width, row1.height + row2.height))
final_image.paste(row1, (0, 0))
final_image.paste(row2, (0, row1.height))

# Save final combined image
output_path = "combined_heatmaps_LAB_CHAMBER.jpg"
final_image.save(output_path)

output_path
