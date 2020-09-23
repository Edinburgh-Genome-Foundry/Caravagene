from caravagene import Part, Construct, ConstructList

my_constructs = ConstructList(
    title="My assemblies",
    note="This is an example.",
    constructs=[
        Construct(
            name="Assembly 1",
            parts=[
                Part("homology-arm", label="HA1"),
                Part("recombinase-recognition-sequence", label="rc1"),
                Part("promoter", label="my promoter"),
                Part("rna-stability-sequence", label="RNA stability"),
                Part("CDS", label="<i>acs</i>"),
                Part("terminator", label="PolyA"),
                Part("insulator", label="I1"),
            ],
        ),
        Construct(
            name="Assembly 2",
            parts=[
                Part("promoter", label="my promoter"),
                Part("CDS", label="gene with a very very long name"),
                Part("terminator", label="PolyA"),
                Part("insulator", label="I1"),
            ],
        ),
    ],
)
my_constructs.to_pdf("multiconstruct.pdf")
