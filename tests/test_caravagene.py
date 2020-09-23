import os
from caravagene import Part, Construct, ConstructList


def test_part():
    part_instance = Part("promoter", label="my promoter")
    part_instance.style
    Part.from_dict(
        {
            "category": "promoter",
            "label": "my promoter",
            "subscript": "p12",
            "reversed": False,
            "sublabel": "lorem ipsum",
            "bg_color": "none",
        }
    )


def test_construct():
    construct_from_dict = Construct.from_dict(
        {
            "parts": [
                {
                    "category": "promoter",
                    "label": "my promoter",
                    "subscript": "p12",
                    "reversed": False,
                    "sublabel": "lorem ipsum",
                    "bg_color": "none",
                }
            ],
            "name": "Test construct",
            "note": "Test note",
        }
    )

    construct = Construct(
        [
            Part("promoter", label="my promoter"),
            Part("CDS", label="gene with a very very long name"),
            Part("terminator", label="PolyA"),
            Part("insulator", label="I1"),
        ],
        name="Test construct",
        note="Test note",
    )
    assert construct.name == "Test construct"
    assert construct.note == "Test note"


def test_constructlist(tmpdir):
    constructs_from_dict = {
        "constructs": [
            {
                "parts": [
                    {
                        "category": "promoter",
                        "label": "my promoter",
                        "subscript": "p12",
                        "reversed": False,
                        "sublabel": "lorem ipsum",
                        "bg_color": "none",
                    }
                ],
                "name": "Test construct",
                "note": "Test note",
            }
        ]
    }

    constructs_from_spreadsheet = ConstructList(
        os.path.join("tests", "from_spreadsheet.xlsx")
    )

    constructs = ConstructList(
        [
            Construct(
                [
                    Part("promoter", label="my promoter"),
                    Part("CDS", label="gene with a very very long name"),
                    Part("terminator", label="PolyA"),
                    Part("insulator", label="I1"),
                ]
            )
        ]
    )

    constructs.to_image(os.path.join(str(tmpdir), "construct.jpeg"))
    constructs.to_html(os.path.join(str(tmpdir), "construct.html"))
    # This won't run on a headless server (Travis CI) but can be tested locally:
    # see more details at https://github.com/wkhtmltopdf/wkhtmltopdf/issues/2037
    # constructs.to_pdf(os.path.join(str(tmpdir), "construct.pdf"))
