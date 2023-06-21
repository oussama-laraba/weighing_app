import sys
# setting path
sys.path.append('../weighing')
import barcode
from barcode.writer import ImageWriter
from sys import platform
import os
from PIL import Image
import pdfkit
from pdf2image import convert_from_path

print(platform)
if platform in ['win32','win64']:
    path_to_wkhtmltopdf = "C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"
else:
    path_to_wkhtmltopdf = r'/usr/bin/wkhtmltopdf'

def gen_bar_code(sequence, path_to_wkhtmltopdf =path_to_wkhtmltopdf, 
                    path_to_file = 'static/html/bar_code.html'  ):
    
    barcode_format = barcode.get_barcode_class('code128')
    my_barcode = barcode_format(sequence, writer=ImageWriter('PNG'))
    my_barcode.save("static/images/bar_code")
    my_barcode = Image.open('static/images/bar_code.png')
    
    config = pdfkit.configuration(wkhtmltopdf = path_to_wkhtmltopdf)
    pdfkit.from_file(path_to_file, output_path = 'static/pdf/bar_code.pdf', configuration = config , options = {"enable-local-file-access": ""})


def print_bar_code(sequence ,path_to_file = 'static/images/barcode.pdf'):
    gen_bar_code(sequence)    
    os.system(f"lpr -P canonG3010Series {path_to_file}")


def write_html(path, content ):
    filled_html = open(rf'{path}', "w")
    filled_html.write(" ")
    filled_html.write(content)
    filled_html.close()


def fill_html_templates( product_name,lot,weight,uom,qte,extra_info, size = 5.82, padding_LR = 10,):
    html_file = open(r'static/html/template.html', "r")
    template = html_file.read()
    html_file.close()
    dict = {'product_name':product_name,'product_lot':lot,
            'product_weight':weight ,'product_uom':uom ,'product_unit_qte': qte, 'Extra_info':extra_info}
    filled_template = template
    for key in dict.keys():
        filled_template = filled_template.replace(f'[{key}]' , f'{dict[key]}')

    write_html(path = 'static/html/display_filled_template.html',content = filled_template)
    ######## adjust the size of the filled html
    width = (size  *45)   - (padding_LR*2)# 1cm ~= 45 px
    bar_code_size = width*0.46 

    body_style = f"margin:0;border:solid;padding:0px {padding_LR}px;width:{width}px;"
    img_style = f"width:{bar_code_size}px;height:{bar_code_size}px;"

    filled_template = filled_template.replace("margin:0;border:solid;padding:0px 10px;width:200px;" ,body_style)
    filled_template = filled_template.replace("width:110px;height:110px;" ,img_style)

    write_html(path = 'static/html/filled_template.html',content = filled_template)

    ## Convert html to pdf 
    config = pdfkit.configuration(wkhtmltopdf = path_to_wkhtmltopdf)
    pdfkit.from_file('static/html/filled_template.html', output_path='static/pdf/filled_template.pdf', configuration=config , options={"enable-local-file-access": ""})
    pdfkit.from_file('static/html/display_filled_template.html', output_path='static/pdf/display_filled_template.pdf', configuration=config , options={"enable-local-file-access": ""})

def gen_display_filled_template_snapshot(): 
    images = ''    
    if platform in ['win32','win64']:
        images = convert_from_path(os.path.join('static/pdf', "display_filled_template.pdf"),poppler_path=r'C:\\Program Files\\poppler-0.68.0\\bin' )

    else:
        images = convert_from_path('static/pdf/display_filled_template.pdf')
    
    width,height = images[0].size
    left,top,right,bottom = 60,60,width/3.5,height/2.6

    filled_template_snapshot = images[0].crop((left, top, right, bottom))
    filled_template_snapshot.save(r'static/images/display_filled_template.png' )

# fill_html_templates('Bobine','00000007',1000,'Kg', 2000,'info supplementaireee')
# gen_display_filled_template_snapshot()