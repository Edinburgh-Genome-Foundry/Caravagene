from caravagene import Part, Construct, ConstructList

constructs = ConstructList([Construct([
    Part('my promoter', category='promoter'),
    Part('gene with a very very long name', category='CDS'),
    Part('PolyA', category='terminator'),
    Part('I1', category='insulator')
])])
constructs.to_image('construct.jpeg')
