import sys
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
    # Export to .dot file for visualization
    dot_folder = join(this_folder, 'dotexport')
    if not os.path.exists(dot_folder):
        os.mkdir(dot_folder)

    # Command line arguments
    file_path = sys.argv[1]
    # Extract a file from a path.
    extracted_file = os.path.split(file_path)[1]
    # Split extracted file to file name and file extension
    file_name_extension = extracted_file.split(".")
    file_name = file_name_extension[0]
    file_extension = file_name_extension[1]

    # Get meta-model from language description
    if(file_extension=='scrp'):
        metamodel = metamodel_from_file(join(grammar_folder, 'scraper.tx'), debug=debug)
    else:
        metamodel = metamodel_from_file(join(grammar_folder, 'report.tx'), debug=debug)
    
    # Optionally export meta-model to dot
    metamodel_export(metamodel, join(dot_folder, f'{file_name}_metamodel.dot'))
    # Optionally export meta-model to png and pdf
    graphs = pydot.graph_from_dot_file(join(dot_folder, f'{file_name}_metamodel.dot'))
    graph = graphs[0]
    # Optionally export meta-model to png
    graph.write_png(join(dot_folder, f'{file_name}_metamodel.png'))
    # Optionally export meta-model to pdf
    graph.write_pdf(join(dot_folder, f'{file_name}_metamodel.pdf'))

    # Instantiate model
    model = metamodel.model_from_file(file_path)

    # Optionally export model to dot
    model_export(model, join(dot_folder, f'{file_name}_model.dot'))
    # Optionally export model to png and pdf
    graphs = pydot.graph_from_dot_file(join(dot_folder, f'{file_name}_model.dot'))
    graph = graphs[0]
    # Optionally export model to png
    graph.write_png(join(dot_folder, f'{file_name}_model.png'))
    # Optionally export model to pdf
    graph.write_pdf(join(dot_folder, f'{file_name}_model.pdf'))


if __name__ == '__main__':
    main()