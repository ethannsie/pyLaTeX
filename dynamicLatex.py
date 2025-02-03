import numpy as np
from pylatex import Document, Section, Subsection, Math, TikZ, Axis, Plot, Figure, Matrix, Alignat
import os
from pylatex.base_classes import Environment
from pylatex.utils import NoEscape
from pathlib import Path
from datetime import datetime
import fitz  # PyMuPDF
from PIL import Image
import subprocess

class Align(Environment):
    _latex_name = 'align'
    packages = [NoEscape(r'\usepackage{amsmath}')]

# Function to convert PDF to images
def pdf_to_images(pdf_path, output_folder):
    pdf_document = fitz.open(pdf_path)
    os.makedirs(output_folder, exist_ok=True)

    for page_number in range(len(pdf_document)):
        page = pdf_document[page_number]
        pixmap = page.get_pixmap()
        img = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)
        output_path = os.path.join(output_folder, f"page_{page_number + 1}.png")
        img.save(output_path, "PNG")
        os.chmod(output_path, 0o644)
        print(f"Saved: {output_path}")

    print("PDF conversion complete!")

# Function to render images in HTML
def imageRender(image_folder, output_file):
    image_files = [f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg', '.gif'))]

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

    with open(output_file, "w") as file:
        file.write(html_content)

    print(f"HTML file generated successfully: {output_file}")

# Function to convert LaTeX to HTML using Pandoc
def convert_latex_to_html(input_tex_file, output_html_file):
    try:
        command = [
            "pandoc",
            input_tex_file,
            "-s",  # standalone
            "--katex",  # use KaTeX for math rendering
            "-o", output_html_file
        ]

        subprocess.run(command, check=True)
        print(f"HTML file generated successfully: {output_html_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error during Pandoc conversion: {e}")
    except FileNotFoundError:
        print("Pandoc is not installed or not found in PATH.")

def run():
    # Define image path and check if it exists
    image_filename = next(Path('.').rglob('kitten.jpg'), None)
    if not os.path.exists(image_filename):
        raise FileNotFoundError(f"Image file not found: {image_filename}")
    image_filename = str(image_filename.resolve())

    # Output directory and filenames
    output_directory = "templates"
    tex_filename = os.path.join(output_directory, "dynamic")
    html_filename = os.path.join(output_directory, "dynamic")

    # Document geometry options
    geometry_options = {"tmargin": "1cm", "lmargin": "10cm"}

    # Create the LaTeX document and write to dynamic.tex
    doc = Document(geometry_options=geometry_options)

    a = np.array([[100, 10, 20]]).T  # Column vector (3x1)
    M = np.matrix([[2, 3, 4],
                   [0, 0, 1],
                   [0, 0, 2]])         # Matrix (3x3)

    with doc.create(Section('The fancy stuff')):
        with doc.create(Subsection('Correct matrix equations')):
            doc.append(Math(data=[Matrix(M), Matrix(a), '=', Matrix(M * a)]))
        with doc.create(Subsection('Align math environment')):
            with doc.create(Align()):
                doc.append(NoEscape(r'\frac{a}{b} &= 0 \\'))
                doc.append(NoEscape(r'x &= y + z \\'))

                # agn.extend([Matrix(M), Matrix(a), '&=', Matrix(M * a)])

        # with doc.create(Subsection('Beautiful graphs')):
        #     with doc.create(TikZ()):
        #         plot_options = 'height=4cm, width=6cm, grid=major'
        #         with doc.create(Axis(options=plot_options)) as plot:
        #             plot.append(Plot(name='model', func='-x^5 - 242'))
        #
        #             coordinates = [
        #                 (-4.77778, 2027.60977),
        #                 (-3.55556, 347.84069),
        #                 (-2.33333, 22.58953),
        #                 (-1.11111, -493.50066),
        #                 (0.11111, 46.66082),
        #                 (1.33333, -205.56286),
        #                 (2.55556, -341.40638),
        #                 (3.77778, -1169.24780),
        #                 (5.00000, -3269.56775),
        #             ]
        #
        #             plot.append(Plot(name='estimate', coordinates=coordinates))
        #
        # with doc.create(Subsection('Cute kitten pictures')):
        #     with doc.create(Figure(position='h!')) as kitten_pic:
        #         kitten_pic.add_image(image_filename, width='120px')
        #         kitten_pic.add_caption("Look it's on its back")

    try:
        # Generate the LaTeX file instead of PDF
        doc.generate_tex(f"{tex_filename}")
        print(f"LaTeX file generated successfully: {tex_filename}")

        # Convert the LaTeX file to HTML using Pandoc
        print(f"{tex_filename}")
        convert_latex_to_html(f"{tex_filename}.tex", f"{html_filename}.html")

    except Exception as e:
        print(f"Error generating LaTeX or HTML: {e}")
