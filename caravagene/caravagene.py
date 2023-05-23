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
with open(os.path.join(THIS_DIR, "template.html"), "r") as f:
    TEMPLATE = template = Template(f.read())
SYMBOL_FILES = {
    s.lower().split(".")[0]: os.path.join(DEFAULT_SYMBOLS_DIR, s)
    for s in os.listdir(DEFAULT_SYMBOLS_DIR)
}


class Part:
    """Represent a genetic part.

    Parameters
    ----------
    category
      Either 'promoter', 'CDS'... Defines the symbol displayed for this part.

    label
      String that will be displayed on top of the part.

    sublabel
      Note that will be written in grey below the label.

    subscript
      Note that will be written below the part.

    reversed
      True/False. Whether the part is in direct or indirect sense.

    bg_color
      String representing any html color, which will be used as background
      to highlight this part.
    """

    def __init__(
        self,
        category,
        label="",
        sublabel="",
        subscript="",
        reversed=False,
        bg_color="none",
    ):
        """Initialize."""
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
        """Define the CSS style from the part's parameters."""
        return "; ".join(
            [
                "background-color: %s" % self.bg_color,
                "background-image: url(%s)" % self.url,
            ]
        )

    @staticmethod
    def from_dict(part_dict):
        """Create a part from a dictionary.

        This is intended for Schema imports from JSON in web applications.
        This dictionary should have the same parameters as the __init__
        function (other parameters will be ignored).
        """
        return Part(
            **dict(
                (d, part_dict[d])
                for d in [
                    "category",
                    "label",
                    "subscript",
                    "reversed",
                    "sublabel",
                    "bg_color",
                ]
                if d in part_dict
            )
        )


class Construct:
    """Represent a genetic construct with several parts.

    Parameters
    ----------
    parts
      A list of Parts, in the order in which they appear in the construct.
      Alternatively, a pandas dataframe can be provided, with columns
      'label', 'category', 'sublabel', 'subscript', 'style'. The last column,
      'style' can be for instance "bg:green bold".

    name
      Name of the construct. Will be displayed on top of the construct's plot.

    note
      Some text that will be displayed between the construct's name and plot.
    """

    def __init__(self, parts, name="", note=""):
        """Initialize."""
        if isinstance(parts, pandas.DataFrame):

            def get_attr(row, attr, default=""):
                if not hasattr(row, attr):
                    return default
                value = getattr(row, attr, "")
                return "" if (str(value) == "nan") else value

            def row_to_part(row):
                bg_color = get_attr(row, "bg_color", "none")
                bg_color = {
                    "blue": "#ECF3FF",
                    "green": "#DFFFE3",
                    "red": "#FFEBE9",
                }.get(bg_color, bg_color)
                part = Part(
                    label=get_attr(row, "label"),
                    category=row.category,
                    reversed=get_attr(row, "reversed", False),
                    bg_color=bg_color,
                    subscript=get_attr(row, "subscript"),
                    sublabel=get_attr(row, "sublabel"),
                )
                style = get_attr(row, "style")
                if style != "":
                    style = str(row.style)
                    if "bold" in style:
                        part.label = "<b>%s</b>" % part.label
                return part

            parts = [row_to_part(row) for i, row in parts.iterrows()]
        self.parts = parts
        self.name = name
        self.note = note

    @staticmethod
    def from_dict(cst_dict):
        """Create a construct from a dictionary.

        This is intended for Schema imports from JSON in web applications.
        This dictionary should have the same parameters as the __init__
        function (other parameters will be ignored).
        """
        return Construct(
            parts=[Part.from_dict(part) for part in cst_dict["parts"]],
            name=cst_dict["name"],
            note=cst_dict["note"],
        )


class ConstructList:
    """Represent a genetic construct will several parts.

    Parameters
    ----------
    constructs
      A list of Constructss, in the order in which they appear in the plot.
      Alternatively, a path to an excel spreadsheet can be provided (see docs
      for explanations on the spreadsheet format).

    title
      Title for this list of constructs. Will be displayed on top of the plots.

    note
      Some text that will be displayed between the title and the plots.

    size
      Size of the font for labels, which also scales the size of sublabel,
      subscript, and the symbol itself.

    orientation
      'portrait' or 'landscape'. Orientation of the page when exporting to PDF.

    page_size
      Page format when exporting to PDF.

    width
      Page width when exporting to an image.

    font
      Name of the font to use for all texts.

    use_google_fonts
      Whether the font should be obtained from Google Fonts (will only work
      with an Internet access).
    """

    def __init__(
        self,
        constructs,
        title="auto",
        note="",
        size=13,
        font="Helvetica",
        orientation="portrait",
        width=600,
        page_size="A4",
        use_google_fonts=False,
    ):
        """Initialize."""
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
                raise ImportError("Install Pandas to read from spreadsheets.")
            if title == "auto":
                self.title = os.path.splitext(os.path.basename(constructs))[0]
                self.title = self.title.replace("_", " ")
            sheet_names = pandas.ExcelFile(constructs, engine="openpyxl").sheet_names
            if "options" in sheet_names:
                df = pandas.read_excel(
                    constructs, sheet_name="options", engine="openpyxl"
                )
                self.__dict__.update(
                    {
                        row.field: row.value
                        for i, row in df.iterrows()
                        if row.field
                        in [
                            "title",
                            "note",
                            "size",
                            "font",
                            "width",
                            "orientation",
                            "page_size",
                        ]
                    }
                )
            constructs = [
                Construct(
                    pandas.read_excel(constructs, sheet_name=sheet, engine="openpyxl"),
                    name=sheet,
                )
                for sheet in sheet_names
                if sheet != "options"
            ]

        if self.title == "auto":
            self.title = ""

        self.constructs = constructs

    @staticmethod
    def from_dict(csts_dict):
        """Create a constructs list from a dictionary.

        This is intended for Schema imports from JSON in web applications.
        This dictionary should have the same parameters as the __init__
        function (other parameters will be ignored).
        """
        return ConstructList(
            constructs=[Construct.from_dict(cst) for cst in csts_dict["constructs"]],
            **dict(
                (d, csts_dict[d])
                for d in [
                    "title",
                    "note",
                    "size",
                    "font",
                    "orientation",
                    "width",
                    "page_size",
                ]
                if d in csts_dict
            )
        )

    def to_html(self, outfile=None):
        """Return a HTML page ready for browser rendering of the plots."""
        result = template.render(
            constructs=self.constructs,
            title=self.title,
            note=self.note,
            size=self.size,
            font=self.font,
            google_font=self.use_google_fonts,
        )
        if outfile is not None:
            with open(outfile, "w+") as f:
                f.write(result)
        else:
            return result

    def to_pdf(self, outfile=None):
        """Return a PDF with all the construct plots.

        If ``outfile`` is not provided, the function returns raw binary PDF
        data as a string.
        """
        if outfile is None:
            outfile = "-"
        process = sp.Popen(
            [
                "wkhtmltopdf",
                "--enable-local-file-access",
                "--quiet",
                "--page-size",
                self.page_size,
                "--orientation",
                self.orientation,
                "-",
                outfile,
            ],
            stdin=sp.PIPE,
            stderr=sp.PIPE,
            stdout=sp.PIPE,
        )
        out, err = process.communicate(self.to_html().encode("utf-8"))
        err = err.decode()
        if (len(err) > 0) and not ("libpng warning" in err):
            raise IOError("Something went wrong while generating the PDF: %s" % err)
        if outfile == "-":
            return out

    def to_image(self, outfile=None, extension=None):
        """Return an image with all the construct plots.

        If ``outfile`` is not provided, the function returns raw binary PDF
        data as a string. In that case the extension ('png', 'jpeg') must be
        provided.
        """
        if outfile is None:
            outfile = "-"
        else:
            extension = os.path.splitext(outfile)[1][1:]
        process = sp.Popen(
            [
                "wkhtmltoimage",
                "--enable-local-file-access",
                "--format",
                extension,
                "--width",
                "%d" % self.width,
                "--disable-smart-width",
                "-",
                outfile,
            ],
            stdin=sp.PIPE,
            stderr=sp.PIPE,
            stdout=sp.PIPE,
        )
        out, err = process.communicate(self.to_html().encode("utf-8"))
        if outfile == "-":
            return out
