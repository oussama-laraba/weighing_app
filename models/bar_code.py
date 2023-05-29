import barcode
from barcode.writer import ImageWriter
import os
from PIL import Image
import pdfkit
from pdf2image import convert_from_path

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

def fill_html_template(product_name,lot,qte,uom,extra_info ):
    html_file = open(r'static/html/template.html', "r")
    template = html_file.read()
    html_file.close()
    
    template = template.replace('{product_name}' , f'{product_name}')
    template = template.replace('{product_lot}' , f'{lot}')
    template = template.replace('{product_qte}' , f'{qte}')
    template = template.replace('{product_uom}' , f'{uom}')
    template = template.replace('{Extra_info}' , f'{extra_info}')

    filled_html_file = open(r'static/html/filled_template.html', "w")
    filled_html_file.write(" ")
    filled_html_file.write(template)
    filled_html_file.close()

    path_to_wkhtmltopdf = r'/usr/bin/wkhtmltopdf'
    config = pdfkit.configuration(wkhtmltopdf = path_to_wkhtmltopdf)
    pdfkit.from_file('static/html/filled_template.html', output_path='static/pdf/filled_template.pdf', configuration=config , options={"enable-local-file-access": ""})

    return filled_html_file

def gen_filled_template_snapshot():

    images = convert_from_path('static/pdf/filled_template.pdf')

    width,height = images[0].size
    left,top,right,bottom = 0,0,width/3.45,height/2.5

    filled_template_snapshot = images[0].crop((left, top, right, bottom))
    filled_template_snapshot.save('static/images/filled_template.png')

fill_html_template('Bobine',178,50,'Unités','Information supplementaire.....' )
gen_filled_template_snapshot()