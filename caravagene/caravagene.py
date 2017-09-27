import os
import re
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

    def __init__(self, category, label='', subscript='', reversed=False,
                 sublabel='', bg_color='none'):
        self.label = label
        self.category = category.lower()
        if self.category not in SYMBOL_FILES:
            raise ValueError("Unkown category " + category)
        self.url = SYMBOL_FILES[self.category]
        self.bg_color = bg_color
        self.subscript = subscript
        self.reversed = reversed
        self.sublabel = sublabel

    @property
    def style(self):
        return "; ".join([
            "background-color: %s" % self.bg_color,
            "background-image: url(%s)" % self.url
        ])


class Construct:

    def __init__(self, parts, name='', note=''):

        if isinstance(parts, pandas.DataFrame):
            def get_attr(row, attr):
                value = getattr(row, attr, '')
                return '' if (str(value) == 'nan') else value
            def row_to_part(row):
                label = get_attr(row, 'label')
                part = Part(label=label, category=row.category,
                            subscript=get_attr(row, 'subscript'),
                            sublabel=get_attr(row, 'sublabel'))
                style = get_attr(row, 'style')
                if style != '':
                    style = str(row.style)
                    if 'bold' in style:
                        part.label = '<b>%s</b>' % part.label
                    color = re.findall(r'bg:(\S+)', style)
                    if len(color) > 0:
                        part.bg_color = {
                            'blue': '#ECF3FF',
                            'green': '#DFFFE3',
                            'red': '#FFEBE9'
                        }.get(color[0], color[0])
                return part
            parts = [row_to_part(row) for i, row in parts.iterrows()]
        self.parts = parts
        self.name = name
        self.note = note


class ConstructList:

    def __init__(self, constructs, title='auto', note='', size=13,
                 font='Raleway', orientation='portrait', width=600,
                 page_size='A4'):

        self.note = note
        self.size = size
        self.font = font
        self.orientation = orientation
        self.width = width
        self.page_size = page_size
        self.title = title

        if isinstance(constructs, str):
            if not PANDAS_INSTALLED:
                raise ImportError("Instal Pandas to read from spreadsheets.")
            if title == 'auto':
                self.title = os.path.splitext(os.path.basename(constructs))[0]
                self.title = self.title.replace('_', ' ')
            sheet_names = pandas.ExcelFile(constructs).sheet_names
            if 'options' in sheet_names:
                df = pandas.read_excel(constructs, sheetname='options')
                self.__dict__.update({
                    row.field: row.value
                    for i, row in df.iterrows()
                    if row.field in ['title', 'note', 'size', 'font', 'width',
                                     'orientation', 'page_size']
                })
            constructs = [
                Construct(pandas.read_excel(constructs, sheetname=sheet),
                          name=sheet)
                for sheet in sheet_names if sheet != 'options'
            ]


        if self.title == "auto":
            self.title = ''

        self.constructs = constructs

    def to_html(self, filepath=None):

        result = template.render(
            constructs=self.constructs, title=self.title, note=self.note,
            size=self.size, font=self.font
        )
        if filepath is not None:
            with open(filepath, 'w+') as f:
                f.write(result)
        else:
            return result

    def to_pdf(self, outfile):
        if outfile is None:
            outfile = '-'
        process = sp.Popen(
            ["wkhtmltopdf", '--quiet', '--page-size', self.page_size,
             '--orientation', self.orientation, '-', outfile],
             stdin=sp.PIPE, stderr=sp.PIPE, stdout=sp.PIPE
        )
        out, err = process.communicate(self.to_html().encode())
        if len(err):
            print (err)
        if outfile is None:
            return out

    def to_image(self, outfile=None, extension=None):
        if outfile is None:
            outfile = '-'
        else:
            extension = os.path.splitext(outfile)[1][1:]
        process = sp.Popen(
            ["wkhtmltoimage",
             "--format", extension,
             "--width", "%d" % self.width,
             "--disable-smart-width",
             '-', outfile],
             stdin=sp.PIPE, stderr=sp.PIPE, stdout=sp.PIPE)
        out, err = process.communicate(self.to_html().encode('utf-8'))
        if outfile is None:
            return out
