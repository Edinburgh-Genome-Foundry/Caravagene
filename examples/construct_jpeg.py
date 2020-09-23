from caravagene import Part, Construct, ConstructList

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

constructs.to_image("construct.jpeg")
