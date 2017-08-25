from caravagene import Part, Construct, ConstructList

my_constructs = ConstructList(
    title="My constructs",
    constructs=[
        Construct(name="ASM1", parts=[
            Part('HA1', category='homology-arm'),
            Part('rc1', category='recombinase-recognition-sequence'),
            Part('my promoter', category='promoter'),
            Part('RNA stability', category='rna-stability-sequence'),
            Part('<i>acs</i>', category='CDS'),
            Part('PolyA', category='terminator'),
            Part('I1', category='insulator'),
        ]),
        Construct(name="ASM2", parts=[
            Part('my promoter', category='promoter'),
            Part('gene with a very very long name', category='CDS'),
            Part('PolyA', category='terminator'),
            Part('I1', category='insulator')
        ])
    ]
)
my_constructs.to_pdf('multiconstruct.pdf')
