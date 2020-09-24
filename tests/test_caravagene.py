import os
from caravagene import Part, Construct, ConstructList


def test_part():
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

    part_instance = Part("promoter", label="my promoter")
    assert part_instance.category == "promoter"
    assert part_instance.label == "my promoter"
    assert part_instance.reversed is False
    assert part_instance.style


def test_construct():
    Construct.from_dict(
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
    assert len(construct.parts) == 4


def test_constructlist(tmpdir):
    ConstructList.from_dict(
        {
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
    )

    ConstructList(os.path.join("tests", "from_spreadsheet.xlsx"))

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
        ],
        note="This is a note",
    )

    assert constructs.note == "This is a note"
    assert constructs.orientation == "portrait"
    assert constructs.page_size == "A4"
    assert constructs.size == 13
    assert constructs.width == 600

    constructs.to_image(os.path.join(str(tmpdir), "construct.jpeg"))
    constructs.to_html(os.path.join(str(tmpdir), "construct.html"))
    # This won't run on a headless server (Travis CI) but can be tested locally:
    # see more details at https://github.com/wkhtmltopdf/wkhtmltopdf/issues/2037
    # constructs.to_pdf(os.path.join(str(tmpdir), "construct.pdf"))
