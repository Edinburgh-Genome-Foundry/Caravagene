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

    @staticmethod
    def from_dict(part_dict):
        return Part(**dict((d, part_dict[d]) for d in [
            'category', 'label', 'subscript', 'reversed',
            'sublabel', 'bg_color'
        ] if d in part_dict))


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

    @staticmethod
    def from_dict(cst_dict):
        return Construct(
            parts = [Part.from_dict(part)
                     for part in cst_dict['parts']],
            name=cst_dict['name'],
            note=cst_dict['note']
        )


class ConstructList:

    def __init__(self, constructs, title='auto', note='', size=13,
                 font='Helvetica', orientation='portrait', width=600,
                 page_size='A4', use_google_fonts=False):

        self.note = note
        self.size = size
        self.font = font
        self.orientation = orientation
        self.width = width
        self.page_size = page_size
        self.title = title
        self.use_google_fonts = use_google_fonts

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

    @staticmethod
    def from_dict(csts_dict):
        return ConstructList(
            constructs=[Construct.from_dict(cst)
                        for cst in csts_dict['constructs']],
            **dict((d, csts_dict[d]) for d in [
                'title', 'note', 'size', 'font', 'orientation',
                'width', 'page_size'
            ] if d in csts_dict)
        )

    def to_html(self, outfile=None):

        result = template.render(
            constructs=self.constructs, title=self.title, note=self.note,
            size=self.size, font=self.font, google_font=self.use_google_fonts
        )
        if outfile is not None:
            with open(outfile, 'w+') as f:
                f.write(result)
        else:
            return result

    def to_pdf(self, outfile=None):
        if outfile is None:
            outfile = '-'
        process = sp.Popen(
            ["wkhtmltopdf", '--quiet', '--page-size', self.page_size,
             '--load-media-error-handling', "ignore",
             '--orientation', self.orientation, '-', outfile],
            stdin=sp.PIPE, stderr=sp.PIPE, stdout=sp.PIPE
        )
        out, err = process.communicate(self.to_html().encode('utf-8'))
        if len(err) > 0:
            raise IOError("Something went wrong while generating the PDF: %s"
                          % err)
        if outfile == '-':
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
