import numpy as np
from pylatex import Document, Section, Subsection, Math, TikZ, Axis, Plot, Figure, Matrix, Alignat
import os
from pathlib import Path
from datetime import datetime
import fitz  # PyMuPDF
from PIL import Image
import os

# Function to convert PDF to images
def pdf_to_images(pdf_path, output_folder):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)

    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Iterate through each page in the PDF
    for page_number in range(len(pdf_document)):
        # Get the page
        page = pdf_document[page_number]

        # Render the page into a pixmap (image)
        pixmap = page.get_pixmap()

        # Convert pixmap to PIL Image
        img = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)

        # Save the image as PNG (or any other format)
        output_path = os.path.join(output_folder, f"page_{page_number + 1}.png")
        img.save(output_path, "PNG")
        os.chmod(output_path, 0o644)
        print(f"Saved: {output_path}")


    print("PDF conversion complete!")

def imageRender(image_folder, output_file):
    # Get all image files in the folder
    image_files = [f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg', '.gif'))]

    # Generate HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Image Gallery</title>
        <style>
            img {{
                max-width: 200px;
                margin: 10px;
            }}
            .gallery {{
                display: flex;
                flex-wrap: wrap;
                gap: 10px;
            }}
        </style>
    </head>
    <body>
        <h1>Image Gallery</h1>
        <div class="gallery">
    """

    for image_file in image_files:
        html_content += f'        <img src="pdfPages/{image_file}" alt="{image_file}">\n'

    html_content += """
        </div>
    </body>
    </html>
    """

    # Write the HTML content to a file
    with open(output_file, "w") as file:
        file.write(html_content)

    print(f"HTML file generated successfully: {output_file}")


if __name__ == '__main__':
    # Define image path and check if it exists
    image_filename = next(Path('.').rglob('kitten.jpg'), None)
    if not os.path.exists(image_filename):
        raise FileNotFoundError(f"Image file not found: {image_filename}")
    image_filename = str(image_filename.resolve())

    month_day = datetime.now().strftime("%m_%d")
    if not os.path.exists("templates/" + month_day):
        os.mkdir("templates/" + month_day)
    # Get current timestamp for unique filenames
    timestamp = datetime.now().strftime("%H_%M_%S")

    # Document geometry options
    geometry_options = {"tmargin": "1cm", "lmargin": "10cm"}
    doc = Document(geometry_options=geometry_options)

    # Define matrices using numpy
    a = np.array([[100, 10, 20]]).T  # Column vector (3x1)
    M = np.matrix([[2, 3, 4],
                   [0, 0, 1],
                   [0, 0, 2]])         # Matrix (3x3)

    # Add content to the document
    with doc.create(Section('The fancy stuff')):
        with doc.create(Subsection('Correct matrix equations')):
            doc.append(Math(data=[Matrix(M), Matrix(a), '=', Matrix(M * a)]))

        with doc.create(Subsection('Alignat math environment')):
            with doc.create(Alignat(numbering=False, escape=False)) as agn:
                agn.append(r'\frac{a}{b} &= 0 \\')
                agn.extend([Matrix(M), Matrix(a), '&=', Matrix(M * a)])

        with doc.create(Subsection('Beautiful graphs')):
            with doc.create(TikZ()):
                plot_options = 'height=4cm, width=6cm, grid=major'
                with doc.create(Axis(options=plot_options)) as plot:
                    plot.append(Plot(name='model', func='-x^5 - 242'))

                    coordinates = [
                        (-4.77778, 2027.60977),
                        (-3.55556, 347.84069),
                        (-2.33333, 22.58953),
                        (-1.11111, -493.50066),
                        (0.11111, 46.66082),
                        (1.33333, -205.56286),
                        (2.55556, -341.40638),
                        (3.77778, -1169.24780),
                        (5.00000, -3269.56775),
                    ]

                    plot.append(Plot(name='estimate', coordinates=coordinates))

        with doc.create(Subsection('Cute kitten pictures')):
            with doc.create(Figure(position='h!')) as kitten_pic:
                kitten_pic.add_image(image_filename, width='120px')
                kitten_pic.add_caption("Look it's on its back")

    output_directory = f"templates/{month_day}/{timestamp}"
    os.makedirs(output_directory)
    output_filename = os.path.join(output_directory, f'latexFile')

    try:
        doc.generate_pdf(output_filename, clean_tex=False)
        print(f"PDF generated successfully: {output_filename}.pdf")
    except Exception as e:
        print(f"Error generating PDF: {e}")

    # Input PDF and output folder
    pdf_path = f"{output_directory}/latexFile.pdf"
    output_dir = f"{output_directory}/pdfPages"
    os.makedirs(output_dir, exist_ok=True)

    # Convert PDF to images
    pdf_to_images(pdf_path, output_dir)

    image_folder = f"{output_directory}/pdfPages"
    output_file = f"{output_directory}/render_pdf.html"
    imageRender(image_folder, output_file)
