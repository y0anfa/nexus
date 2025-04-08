import click
import os
import sys
from pathlib import Path
from converter import convert_markdown_to_pdf
from config import load_config, validate_config, get_default_config

# Get version from pyproject.toml if available
try:
    import tomli
    with open(Path(__file__).parent / 'pyproject.toml', 'rb') as f:
        version = tomli.load(f).get('project', {}).get('version', '0.1.0')
except (ImportError, FileNotFoundError):
    version = '0.1.0'

@click.group()
@click.version_option(version)
def cli():
    """
    Nexus - A tool to convert markdown files to professionally styled PDFs.
    
    This CLI provides commands to convert individual markdown files or batch
    process directories of markdown files into PDF documents with consistent styling.
    """
    pass

@cli.command()
@click.option('--input', '-i', type=click.Path(exists=True), required=True, help='Path to the input markdown file')
@click.option('--output', '-o', type=click.Path(), required=True, help='Path to the output PDF file')
@click.option('--template', '-t', type=click.Path(exists=True), required=False, help='Path to the Jinja2 template file')
@click.option('--config', '-c', type=click.Path(exists=True), required=False, help='Path to the config file')
@click.option('--save-html', is_flag=True, help='Save intermediate HTML file for debugging')
def convert(input, output, template, config, save_html):
    """
    Convert a single markdown file to PDF.
    
    This command takes a markdown file and converts it to a PDF document using
    a specified template and configuration. If no template is specified, a default
    template will be used if available.
    """
    try:
        # Load and validate config
        if config:
            config_data = load_config(config)
        else:
            config_data = {}
            
        # Set save_html flag in config if specified
        if save_html:
            config_data['save_html'] = True
            
        # Validate and set defaults
        config_data = validate_config(config_data)
        
        # Convert the file
        convert_markdown_to_pdf(input, output, template, config_data)
        click.echo(f"Successfully converted {input} to {output}")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)

@cli.command()
@click.option('--input-dir', '-i', type=click.Path(exists=True, file_okay=False, dir_okay=True), required=True, 
              help='Directory containing markdown files')
@click.option('--output-dir', '-o', type=click.Path(file_okay=False, dir_okay=True), required=True, 
              help='Directory for output PDF files')
@click.option('--template', '-t', type=click.Path(exists=True), required=False, help='Path to the Jinja2 template file')
@click.option('--config', '-c', type=click.Path(exists=True), required=False, help='Path to the config file')
@click.option('--save-html', is_flag=True, help='Save intermediate HTML files for debugging')
@click.option('--pattern', '-p', default='*.md', help='Glob pattern to match markdown files (default: *.md)')
def batch_convert(input_dir, output_dir, template, config, save_html, pattern):
    """
    Convert all markdown files in a directory to PDFs.
    
    This command processes all markdown files matching the specified pattern
    in the input directory and converts them to PDF documents in the output directory.
    """
    try:
        # Load and validate config
        if config:
            config_data = load_config(config)
        else:
            config_data = {}
            
        # Set save_html flag in config if specified
        if save_html:
            config_data['save_html'] = True
            
        # Validate and set defaults
        config_data = validate_config(config_data)
        
        # Ensure output directory exists
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True, parents=True)
        
        # Process all markdown files
        input_path = Path(input_dir)
        markdown_files = list(input_path.glob(pattern))
        
        if not markdown_files:
            click.echo(f"No markdown files found in {input_dir} matching pattern '{pattern}'")
            return
        
        click.echo(f"Found {len(markdown_files)} markdown files to process")
        
        for md_file in markdown_files:
            output_file = output_path / f"{md_file.stem}.pdf"
            click.echo(f"Converting {md_file} to {output_file}")
            try:
                convert_markdown_to_pdf(str(md_file), str(output_file), template, config_data)
            except Exception as e:
                click.echo(f"Error converting {md_file}: {str(e)}", err=True)
        
        click.echo(f"Successfully converted {len(markdown_files)} files to PDF")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)

@cli.command()
@click.option('--output', '-o', type=click.Path(), default='config.yaml', help='Path to save the config file')
def init(output):
    """
    Initialize a new configuration file with default settings.
    
    This creates a new YAML configuration file with all the default settings
    that can be customized for your specific needs.
    """
    import yaml
    
    # Get default config
    config = get_default_config()
    
    # Save to file
    with open(output, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)
    
    click.echo(f"Created configuration file at {output}")
    click.echo("Edit this file to customize your PDF output settings.")

if __name__ == "__main__":
    cli()