import numpy as np
from pylatex import Document, Section, Subsection, Math, TikZ, Axis, Plot, Figure, Matrix, Alignat, LongTable, MultiColumn
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

# LATEX GENERATION -----------------------------------------
# LATEX GENERATION
# LATEX GENERATION
def run():
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
                doc.append(NoEscape(r'x &= 3 + z'))

                # agn.extend([Matrix(M), Matrix(a), '&=', Matrix(M * a)])

    with doc.create(LongTable("l l l")) as data_table:
        data_table.add_hline()
        data_table.add_row(["header 1", "header 2", "header 3"])
        data_table.add_hline()
        data_table.end_table_header()
        data_table.add_hline()
        data_table.add_row((MultiColumn(3, align="r", data="Continued on Next Page"),))
        data_table.add_hline()
        data_table.end_table_footer()
        data_table.add_hline()
        data_table.add_row(
            (MultiColumn(3, align="r", data="Not Continued on Next Page"),)
        )
        data_table.add_hline()
        data_table.end_table_last_footer()
        row = ["Content1", "9", "Longer String"]
        for i in range(150):
            data_table.add_row(row)

    try:
        # Generate the LaTeX file instead of PDF
        doc.generate_pdf(f"{tex_filename}")
        doc.generate_tex(f"{tex_filename}")
        print(f"LaTeX file generated successfully: {tex_filename}")

        # Convert the LaTeX file to HTML using Pandoc
        print(f"{tex_filename}")
        convert_latex_to_html(f"{tex_filename}.tex", f"{html_filename}.html")

    except Exception as e:
        print(f"Error generating LaTeX or HTML: {e}")
