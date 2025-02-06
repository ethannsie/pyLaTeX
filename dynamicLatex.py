import numpy as np
from pylatex import Document, Section, Tabularx, Subsection, Math, TikZ, Axis, Plot, Figure, Matrix, Alignat, LongTable, MultiColumn, TikZDraw, Command
import os
from pylatex.base_classes import Environment
from pylatex.utils import NoEscape
from pathlib import Path
from datetime import datetime
import fitz  # PyMuPDF
from PIL import Image
import subprocess
import pandas as pd

class Align(Environment):
    _latex_name = 'align'
    packages = [NoEscape(r'\usepackage{amsmath}')]

def identityMaker(length):
    formatList = []
    for row in range(length):
        row1 = []
        for column in range(length):
            if row == column:
                row1.append(1)
            else:
                row1.append(0)
        formatList.append(row1)
    return np.matrix(formatList)


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
    geometry_options = {"tmargin": "1cm", "lmargin": "1cm", "rmargin": "1cm", "bmargin": "1cm"}

    # Create the LaTeX document and write to dynamic.tex
    doc = Document(geometry_options=geometry_options)

    # # Add title and author information
    # doc.preamble.append(NoEscape(r"""
    # \title{TedTalk – TeX and LaTeX}
    # \author{Ethan Sie and Sascha Gordon-Zolov}
    # \date{February 2025}
    # """))

    # Add heading using direct formatting
    doc.append(NoEscape(r"""
    \noindent \textbf{\LARGE {LaTeX TED Talk}} \\
    \noindent \textbf{Ethan Sie, Sascha Gordon-Zolov \\ Mr. Mykolyk \\ Software Development} \hfill \textbf{February 2025}
    """))



    data = [2,3 ,4 , 2,3 ,4 , 6, 7, 8, 9, 0, 10, 2, 23, 15, 4, 6,3,5 ,4,5 ,6, 34, 3, 654, 7, 456, 3, 45, 754, 3,45 ,45, 345, 345, 345, 6, 7, 8, 9, 0, 10, 2, 23, 2,3 ,4 , 6, 7, 8, 9, 0, 10, 2, 23, 15, 4, 6,3,5 ,4,5 ,6, 34, 3, 654, 7, 456, 3, 45, 754, 3,45 ,45, 345, 345, 345, 15, 4, 6,3,5 ,4,5 ,6, 34, 3, 654, 7, 456, 3, 45, 754, 3,45 ,45, 345, 345, 345]
    print(len(data))

    a = np.array([[100, 10, 20], [30, 40, 6], [5, 6, 0], [10, 2, 5], [10, 40, 3], [10, 2, 5], [1, 2, 7]]).T  # Column vector (3x1)

    formatList = []
    for count, element in enumerate(data):
        if count != 0 and (count+1)%3 == 0:
            formatList.append([data[count-2], data[count-1], element])

    # M = np.matrix([[2, 3, 4],
    #                [0, 0, 1],
    #                [0, 0, 2]])         # Matrix (3x3)
    M = np.matrix(formatList)

    with doc.create(Section('The fancy stuff')):
        with doc.create(Subsection('Correct matrix equations')):
            doc.append(Math(data=[Matrix(M), Matrix(a), '=', Matrix(M * a)]))
            test = np.matrix([[100, -10, 20, -3, 5, 7, 2], [30, 40, 6, 12, -3 ,6, 78], [5, -6, 0, 2, 6, 5, 67], [-10, 2, 5, 123, 6, -657, 3], [10, 40, 3, 1, -5,43 ,75], [10, 2, -5, 234, -346 ,7, 2], [1, 2, 7, 12, -5, 4,7]])
            tester = np.matrix([[-23, 45, 43, -36, 54, -17, 42], [330, -740, 96, 812, 35 ,-63, 784], [53, 26, 30, -42, 56, 65, -6], [0, -22, 35, 13, 56, 67, -33], [170, 0, 35, -41, 55,-433 ,725], [104, 32, -25, 34, 46 ,76, 24], [14, -23, 67, 182, 59, 47,87]])
            dimensions = test.shape
            rows, columns = dimensions
            identity = identityMaker(columns)
            doc.append(Math(data=[Matrix(test), Matrix(identity), '=', Matrix(identity), Matrix(test), '=', Matrix(test * identity)]))
            # test = np.matrix([[12],[3],[3]])
            # tester = np.matrix([[7/6,1/3,5/3],[1,0,1],[1/3,-1/3,1/3]])
            doc.append(Math(data=[Matrix(tester), Matrix(test), '=', Matrix(tester * test)]))
            doc.append(Math(data=[Matrix(test), Matrix(tester), '=', Matrix(test * tester)]))

            # identity = identityMaker(rows)
            # doc.append(Math(data=[Matrix(identity), Matrix(test), '=', Matrix(identity * test)]))

        with doc.create(Subsection('Align math environment')):
            with doc.create(Align()):
                doc.append(NoEscape(r'\frac{a}{b} &= 0 \\'))
                doc.append(NoEscape(r'x &= y + z \\'))
                doc.append(NoEscape(r'x &= 3 + z'))

                # agn.extend([Matrix(M), Matrix(a), '&=', Matrix(M * a)])


    # with doc.create(TikZ()) as tikz:
    #     tikz.append(TikZDraw(["sin(x)"]))

    dataToProcess = []

    df = pd.read_csv('data/summerOly_athletes.csv')
    for i in range(100):
        dataRow = df.loc[i]
        dataToProcess.append([dataRow[0], dataRow[1], dataRow[2], dataRow[3], int(dataRow[4]), dataRow[5], dataRow[6], dataRow[7], dataRow[8]])

    print(identityMaker(4))

    # with doc.create(LongTable("l l l l l l l l l")) as data_table:
    with doc.create(LongTable("p{1.5cm} p{0.5cm} p{2cm} p{1cm} p{1cm} p{1.5cm} p{1.5cm} p{5cm} p{1.5cm}")) as data_table:
        data_table.add_hline()
        data_table.add_row(["header 1", "header 2", "header 3","header 1", "header 2", "header 3","header 1", "header 2", "header 3"])
        data_table.add_hline()
        data_table.end_table_header()
        data_table.add_hline()
        data_table.add_row((MultiColumn(9, align="r", data="Continued on Next Page"),))
        data_table.add_hline()
        data_table.end_table_footer()
        data_table.add_hline()
        data_table.add_row(
            (MultiColumn(9, align="r", data="Not Continued on Next Page"),)
        )
        data_table.add_hline()
        data_table.end_table_last_footer()
        row = ["Content1", "9", "Longer String"]
        for element in dataToProcess:
            data_table.add_row(element)

    try:
        # Generate the LaTeX file instead of PDF
        doc.generate_pdf(f"{tex_filename}")
        doc.generate_tex(f"{tex_filename}")
        print(f"LaTeX file generated successfully: {tex_filename}")

        # Convert the LaTeX file to HTML using Pandoc
        print(f"{tex_filename}")
        convert_latex_to_html(f"{tex_filename}.tex", f"{html_filename}.html")

        pdf_to_images("templates/dynamic.pdf", "templates/dynamic_pdf")
    except Exception as e:
        print(f"Error generating LaTeX or HTML: {e}")
