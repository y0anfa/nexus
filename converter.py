import markdown
import jinja2
import pdfkit
from pathlib import Path
from datetime import datetime
import os

def convert_markdown_to_pdf(input_file, output_file, template_path=None, config=None):
    """
    Convert a markdown file to PDF using a template.
    
    Args:
        input_file (str): Path to the input markdown file
        output_file (str): Path to save the output PDF file
        template_path (str, optional): Path to the Jinja2 template file. If not provided,
                                      will try to find a default template.
        config (dict, optional): Configuration dictionary with settings for the PDF
        
    Returns:
        None
    """
    # Set default config if not provided
    if config is None:
        from config import get_default_config, validate_config
        config = validate_config({})
    
    # Read the markdown file
    with open(input_file, 'r') as file:
        markdown_content = file.read()

    # Convert markdown to HTML
    # This uses Python's markdown library to parse markdown to HTML
    html_content = markdown.markdown(markdown_content, extensions=['tables', 'fenced_code'])

    # Determine the template path
    if not template_path:
        # Look in various locations for a default template
        possible_locations = [
            # Current directory
            Path('template.html'),
            # Templates directory
            Path(__file__).parent / 'templates' / 'default.html'
        ]
        
        for location in possible_locations:
            if location.exists():
                template_path = location
                break
        
        if not template_path:
            raise FileNotFoundError("No default template found. Please specify a template path.")

    # Render the template with the HTML content
    template = jinja2.Template(Path(template_path).read_text())
    html_output = template.render(
        content=html_content,
        company=config.get("company"),
        logo=config.get("logo"),
        version=config.get("version"),
        date=config.get("date"),
        author=config.get("author"),
        approved_by=config.get("approved_by"),
        comments=config.get("comments"),
        title=config.get("title"),
    )

    # Create temporary HTML file for debugging if needed
    if config.get("save_html", False):
        html_output_path = f"{os.path.splitext(output_file)[0]}.html"
        with open(html_output_path, "w") as f:
            f.write(html_output)

    # Convert HTML to PDF using pdfkit
    pdfkit.from_string(
        html_output, 
        output_file,
        options=config.get("pdf_options", {})
    )
    
              