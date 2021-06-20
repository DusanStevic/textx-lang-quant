import os
import pydot
from os.path import dirname, join
from textx import metamodel_from_file
from textx.export import metamodel_export, model_export
# Set GraphViz Path variable
os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin'

def main(debug=False):

    this_folder = dirname(__file__)
    grammar_folder = join(this_folder, 'grammar')
    examples_folder = join(this_folder, 'examples')
    # Export to .dot file for visualization
    dot_folder = join(this_folder, 'dotexport')
    if not os.path.exists(dot_folder):
        os.mkdir(dot_folder)

    # Get meta-model from language description
    scraper_metamodel = metamodel_from_file(join(grammar_folder, 'scraper.tx'), debug=debug)
    
    # Optionally export meta-model to dot
    metamodel_export(scraper_metamodel, join(dot_folder, 'scraper_metamodel.dot'))
    # Optionally export meta-model to png and pdf
    graphs = pydot.graph_from_dot_file(join(dot_folder, 'scraper_metamodel.dot'))
    graph = graphs[0]
    # Optionally export meta-model to png
    graph.write_png(join(dot_folder, 'scraper_metamodel.png'))
    # Optionally export meta-model to pdf
    graph.write_pdf(join(dot_folder, 'scraper_metamodel.pdf'))

    # Instantiate model
    scraper_model = scraper_metamodel.model_from_file(join(examples_folder, 'scraper.scrp'))

    # Optionally export model to dot
    model_export(scraper_model, join(dot_folder, 'scraper_model.dot'))
    # Optionally export model to png and pdf
    graphs = pydot.graph_from_dot_file(join(dot_folder, 'scraper_model.dot'))
    graph = graphs[0]
    # Optionally export model to png
    graph.write_png(join(dot_folder, 'scraper_model.png'))
    # Optionally export model to pdf
    graph.write_pdf(join(dot_folder, 'scraper_model.pdf'))


if __name__ == '__main__':
    main()