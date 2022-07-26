import os
from PIL import Image


def process_pdf(images, bucket, selected_topics, component):
    selected_topic_index = sorted([int(topic.split(' ')[0]) for topic in selected_topics])
    selected_topic_index = [str(i) for i in selected_topic_index]

    if not os.path.isdir('generated_papers'):
        os.makedirs('generated_papers')

    pdf_file_path = f'generated_papers/component{component}_{"-".join(selected_topic_index)}_.pdf'
    download_images(images, bucket)
    convert_to_pdf(images, pdf_file_path)
    upload_pdf(pdf_file_path, bucket)

    return pdf_file_path

def download_images(images, bucket):
    for filename in images:
        blob = bucket.blob(filename)
        os.makedirs(os.path.dirname(filename), exist_ok = True)
        blob.download_to_filename(filename)

def convert_to_rgb(img, size = (1654,2339)):
    # default size = A4
    if len(img.split()==3):
        return img
    rgb = Image.new('RGB', size, (255,255,255))
    rgb.paste(img,mask = img.split()[-1])
    return rgb

def convert_to_pdf(images, pdf_file_path):
    """images: list of str, which has image paths"""
    image_files = []
    for filename in images:
        image_files.append(convert_to_rgb(Image.open(filename)))

    image_files[0].save(pdf_file_path, 'PDF', resolution = 100.0, save_all = True, append_images = image_files[1:])

    
    
def upload_pdf(pdf_file_path, bucket):
    blob = bucket.blob(pdf_file_path)
    blob.upload_from_filename(pdf_file_path)
