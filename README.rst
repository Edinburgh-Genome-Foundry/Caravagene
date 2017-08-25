Caravagene
=============
.. image:: https://raw.githubusercontent.com/Edinburgh-Genome-Foundry/Caravagene/master/logo.png
   :alt: [logo]
   :align: center
   :width: 600px



Caravagene is a Python library to plot schemas of DNA constructs from a list of parts:

.. code:: python

    from caravagene import Part, Construct, ConstructList

    constructs = ConstructList([Construct([
        Part('my promoter', category='promoter'),
        Part('gene with a very very long name', category='CDS'),
        Part('PolyA', category='terminator'),
        Part('I1', category='insulator')
    ])])

    constructs.to_image('construct.jpeg')

.. image:: https://raw.githubusercontent.com/Edinburgh-Genome-Foundry/Caravagene/master/examples/construct.jpeg
   :alt: [logo]
   :align: center
   :width: 600px

Here is another example producing `this PDF <https://raw.githubusercontent.com/Edinburgh-Genome-Foundry/Caravagene/master/examples/multiconstruct.pdf>`_
showing multiple constructs:

.. code:: python

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

.. image:: https://raw.githubusercontent.com/Edinburgh-Genome-Foundry/Caravagene/master/examples/screen_capture.png
   :alt: [logo]
   :align: center
   :width: 600px

It is also possible to add support for other categories/symbols, as follows:

.. code:: python:

    from caravagene import SYMBOL_FILES
    SYMBOL_FILES['my-new-category'] = 'path/to/some/symbol.svg'


Installation
-------------

Caravagene requires `WkHTMLtoPDF <https://wkhtmltopdf.org/>`_ to be installed. On Ubuntu, install it with

.. code:: shell

    (sudo) apt-get install wkhtmltopdf


You can install caravagene through PIP

.. code:: shell

    sudo pip install caravagene

Alternatively, you can unzip the sources in a folder and type

.. code:: shell

    sudo python setup.py install


Licence
--------

Caravagene is an open-source software originally written at the `Edinburgh Genome Foundry
<http://www.genomefoundry.org>`_ by `Zulko <https://github.com/Zulko>`_
and `released on Github <https://github.com/Edinburgh-Genome-Foundry/Caravagene>`_ under the MIT licence (copyright Edinburgh Genome Foundry).
Everyone is welcome to contribute !
