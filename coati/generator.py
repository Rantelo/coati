from coati.powerpoint import open_pptx, runpowerpoint
import os
import logging
from colorlog import ColoredFormatter

LOG_LEVEL = logging.DEBUG
LOGFORMAT = "%(asctime)s - %(log_color)s%(message)s"
logging.root.setLevel(LOG_LEVEL)
formatter = ColoredFormatter(LOGFORMAT)
stream = logging.StreamHandler()
stream.setLevel(LOG_LEVEL)
stream.setFormatter(formatter)
log = logging.getLogger('pythonConfig')
log.setLevel(LOG_LEVEL)
log.addHandler(stream)


path = 'builders/'
template_path = 'templates/slide_template.py'
config_template_path = 'templates/generator/config_template.py'

def _get_slides_shapes(ppt_path):
    pptapp = runpowerpoint()
    pptFile = open_pptx(pptapp, ppt_path)
    log.debug('Template opened successfully')

    all_slide_shapes = []
    for slide in pptFile.Slides:
        shapes_in_slide = _get_shapes_in_slide(slide)
        all_slide_shapes.append(shapes_in_slide)

    pptFile.close()
    pptapp.Quit()
    log.debug('Finished reading template')

    return all_slide_shapes

def _get_shapes_in_slide(slide):
    shapes_in_slide = {}
    for each_shape in slide.shapes:
        shapes_in_slide.update({each_shape.name: ()})
    return shapes_in_slide

def generate_path(p):
    if not os.path.exists(os.path.dirname(p)):
        try:
            os.makedirs(os.path.dirname(p))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise

def cp(src, dst, fn):
    source = open(src, 'r')
    result = fn(source.read())
    destination = open(dst, 'w')
    destination.write(result)
    source.close
    destination.close

def insert_code(complete_text, text_to_insert, text_to_replace):
    ans = complete_text.replace(text_to_replace, text_to_insert)
    return ans

def generate(ppt_path):
    spaces = " " * 12
    slide_tuples = '['
    config_filename = path + 'config.py'
    for i, slide in enumerate(_get_slides_shapes(ppt_path)):
        slide_name = 'slide' + str(i+1)
        slide_tuples += ('\n' + spaces if i != 0 else '') + '(' + str(i) + ', ' + slide_name + '.build()),'
        filename = path + slide_name + '.py';
        generate_path(path)
        cp(template_path, filename, lambda source: insert_code(
            source,
            str(slide).replace(", ",",\n" + spaces),
            '"_-{}-_"'))
        if i == 0:
            log.warn('created folder %s', path)
        log.info('created %s', filename)

    cp(config_template_path, config_filename, lambda source: insert_code(
        source,
        (slide_tuples[:-1] + ']'),
        '"_-{}-_"'))
    log.info('created %s', config_filename)