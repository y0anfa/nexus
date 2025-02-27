import markdown
import jinja2
import pdfkit
from pathlib import Path
from datetime import datetime

def convert_markdown_to_pdf(input_file, output_file, template_path=None):
    # Read the markdown file
    with open(input_file, 'r') as file:
        markdown_content = file.read()

    # Convert markdown to HTML
    html_content = markdown.markdown(markdown_content)

    # Load the template
    if not template_path:
        template_path = Path(__file__).parent / 'template.html'

    # Render the template with the HTML content
    template = jinja2.Template(Path(template_path).read_text())
    html_output = template.render(content=html_content)

    # Convert HTML to PDF using pdfkit
    pdfkit.from_string(
        html_output, 
        output_file,
        options={
            'page-size': 'A4',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
        }
    )
    
              