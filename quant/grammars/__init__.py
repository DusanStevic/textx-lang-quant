from os.path import dirname, join
from textx import language, metamodel_from_file
from textx import generator as gen
from ..generator import generate

@language("scraper", "*.scrp")
def scraper_language():
    "A language for acquiring financial time-series"
    return metamodel_from_file(join(dirname(__file__), "scraper.tx"))

@language("reporter", "*.rprt")
def reporter_language():
    "A language for visualizing financial time-series"
    return metamodel_from_file(join(dirname(__file__), "reporter.tx"))

@gen('reporter', 'html+pdf')
def reporter_generate_html(metamodel, model, output_path, overwrite, debug):
    "Generate stock market reports in pdf and html format from the rprt file"
    input_file = model._tx_filename
    generate(input_file)