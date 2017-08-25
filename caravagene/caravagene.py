import os
import subprocess as sp

from jinja2 import Template
try:
    import pandas
    PANDAS_INSTALLED = True
except:
    PANDAS_INSTALLED = False
THIS_DIR = os.path.dirname(os.path.realpath(__file__))
DEFAULT_SYMBOLS_DIR = os.path.join(THIS_DIR, "symbols")
with open(os.path.join(THIS_DIR, "template.html"), 'r') as f:
    TEMPLATE = template = Template(f.read())
SYMBOL_FILES = {
    s.lower().split('.')[0]: os.path.join(DEFAULT_SYMBOLS_DIR, s)
    for s in os.listdir(DEFAULT_SYMBOLS_DIR)
}


class Part:

    def __init__(self, label, category, bg_color='none'):
        self.label = label
        self.category = category.lower()
        if self.category not in SYMBOL_FILES:
            raise ValueError("Unkown category " + category)
        self.url = SYMBOL_FILES[self.category]
        self.style = "; ".join([
            "background-color: %s" % bg_color,
            "background-image: url(%s)" % self.url
        ])


class Construct:

    def __init__(self, parts, name=''):
        if isinstance(parts, pandas.DataFrame):
            parts = [
                Part(label=row.label, category=row.category)
                for i, row in parts.iterrows()
            ]
        self.parts = parts
        self.name = name


class ConstructList:

    def __init__(self, constructs, title='auto'):
        if isinstance(constructs, str):
            if not PANDAS_INSTALLED:
                raise ImportError("Instal Pandas to read from spreadsheets.")
            if title == 'auto':
                title = os.path.splitext(os.path.basename(constructs))[0]
                title = title.replace('_', ' ')
            constructs = [
                Construct(pandas.read_excel(constructs, sheetname=sheet),
                          name=sheet)
                for sheet in pandas.ExcelFile(constructs).sheet_names
            ]
        if title == "auto":
            title = ''
        self.constructs = constructs
        self.title = title

    def to_html(self, size=15, font='Raleway'):
        return template.render(constructs=self.constructs, title=self.title,
                               size=size, font=font)

    def to_pdf(self, outfile, page_size='A4', orientation='portrait'):
        if outfile is None:
            outfile = '-'
        process = sp.Popen(
            ["wkhtmltopdf", '--quiet', '--page-size', page_size,
             '--orientation', orientation, '-', outfile],
             stdin=sp.PIPE, stderr=sp.PIPE, stdout=sp.PIPE
        )
        out, err = process.communicate(self.to_html().encode())
        if len(err):
            print (err)
        if outfile is None:
            return out

    def to_image(self, outfile=None, extension=None, width=600):
        if outfile is None:
            outfile = '-'
        else:
            extension = os.path.splitext(outfile)[1][1:]
        process = sp.Popen(
            ["wkhtmltoimage",
             "--format", extension,
             "--width", "%d" % width,
             "--disable-smart-width",
             '-', outfile],
             stdin=sp.PIPE, stderr=sp.PIPE, stdout=sp.PIPE)
        out, err = process.communicate(self.to_html().encode())
        if outfile is None:
            return out
