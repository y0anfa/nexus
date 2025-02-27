import click
from converter import convert_markdown_to_pdf

@click.command()
@click.option('--input', '-i', type=click.Path(exists=True), required=True, help='Path to the input markdown file')
@click.option('--output', '-o', type=click.Path(), required=True, help='Path to the output PDF file')
@click.option('--template', '-t', type=click.Path(exists=True), required=False, help='Path to the Jinja2 template file')
def convert(input, output, template):
    convert_markdown_to_pdf(input, output, template)
    
if __name__ == "__main__":
    convert()