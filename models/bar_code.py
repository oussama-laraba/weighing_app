import barcode
from barcode.writer import ImageWriter
import os
from PIL import Image
import pdfkit

def gen_bar_code(   sequence , path_to_wkhtmltopdf = r'/usr/bin/wkhtmltopdf' , 
                    path_to_file = 'static/html/bar_code.html'  ):
    
    barcode_format = barcode.get_barcode_class('code128')
    my_barcode = barcode_format(sequence, writer=ImageWriter('PNG'))
    my_barcode.save("static/images/bar_code")
    my_barcode = Image.open('static/images/bar_code.png')
    
    
    
    config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)
    pdfkit.from_file(path_to_file, output_path='static/pdf/bar_code.pdf', configuration=config , options={"enable-local-file-access": ""})


def print_bar_code(sequence ,path_to_file = 'static/images/barcode.pdf'):
    gen_bar_code(sequence)
    
    os.system(f"lpr -P canonG3010Series {path_to_file}")

