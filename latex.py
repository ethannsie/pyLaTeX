import numpy as np
from pylatex import Document, Section, Subsection, Math, TikZ, Axis, Plot, Figure, Matrix, Alignat
import os
from pathlib import Path
from datetime import datetime

if __name__ == '__main__':
    # Define image path and check if it exists
    image_filename = next(Path('.').rglob('kitten.jpg'), None)
    if not os.path.exists(image_filename):
        raise FileNotFoundError(f"Image file not found: {image_filename}")
    image_filename = str(image_filename.resolve())

    # Get current timestamp for unique filenames
    timestamp = datetime.now().strftime("%m_%d_%H_%M_%S")

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

    output_directory = f"templates/output_{timestamp}"
    os.makedirs(output_directory)
    output_filename = os.path.join(output_directory, f'latexFile')

    try:
        doc.generate_pdf(output_filename, clean_tex=False)
        print(f"PDF generated successfully: {output_filename}.pdf")
    except Exception as e:
        print(f"Error generating PDF: {e}")
