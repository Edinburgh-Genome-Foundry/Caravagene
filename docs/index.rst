Caravagene
==========

.. image:: https://raw.githubusercontent.com/Edinburgh-Genome-Foundry/Caravagene/master/logo.png
  :alt: [logo]
  :align: center
  :width: 600px


Caravagene is a Python library to plot schemas of DNA constructs from a list of parts:

.. code:: python

   from caravagene import Part, Construct, ConstructList

   constructs = ConstructList([Construct([
       Part('promoter', label='my promoter'),
       Part('CDS', label='gene with a very very long name'),
       Part('terminator', label='PolyA'),
       Part('insulator', label='I1')
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

.. image:: https://raw.githubusercontent.com/Edinburgh-Genome-Foundry/Caravagene/master/examples/multiconstruct_screen_capture.png
  :alt: [logo]
  :align: center
  :width: 600px

Note that ``ConstructList`` can be supplied with a font. It is also possible to extend Caravagene to support other categories/symbols, as follows:

.. code:: python

    from caravagene import SYMBOL_FILES
    SYMBOL_FILES['my-new-category'] = 'path/to/some/symbol.svg'

Finally, here is an example using an Excel spreadsheet:

**Spreadsheet:**

.. image:: https://raw.githubusercontent.com/Edinburgh-Genome-Foundry/Caravagene/master/examples/from_spreadsheet_sample.png
  :alt: [logo]
  :align: center
  :width: 400px

**Python code:**

.. code:: python

   from caravagene import ConstructList
   my_constructs = ConstructList("my_spreadsheet.xlsx")
   my_constructs.to_pdf('my_schemas.pdf')

or **command-line (one-time use):**

.. code:: shell

   caravagene my_spreadsheet.xlsx my_schemas.pdf

or **command-line (re-render when the spreadsheet changes on disk):**

.. code:: shell

   caravagene my_spreadsheet.xlsx my_schemas.pdf --watch

**Output:**

.. image:: https://raw.githubusercontent.com/Edinburgh-Genome-Foundry/Caravagene/master/examples/from_spreadsheet_screen_capture.png
 :alt: [logo]
 :align: center
 :width: 600px


Installation
-------------

Caravagene requires `WkHTMLtoPDF <https://wkhtmltopdf.org/>`_ to be installed. On Ubuntu, install it with:

.. code:: shell

   (sudo) apt-get install wkhtmltopdf


You can install caravagene through PIP:

.. code:: shell

   sudo pip install caravagene

Alternatively, you can unzip the source code in a folder and type:

.. code:: shell

   sudo python setup.py install


Licence
--------

Caravagene is an open-source software originally written at the `Edinburgh Genome Foundry
<http://www.genomefoundry.org>`_ by `Zulko <https://github.com/Zulko>`_
and `released on Github <https://github.com/Edinburgh-Genome-Foundry/Caravagene>`_ under the MIT licence (Copyright 2017 Edinburgh Genome Foundry).
Everyone is welcome to contribute!



.. raw:: html

       <a href="https://twitter.com/share" class="twitter-share-button"
       data-text="Caravagene - A DNA construct sketching library" data-size="large" data-hashtags="synbio">Tweet
       </a>
       <script>!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0],p=/^http:/.test(d.location)?'http':'https';
       if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src=p+'://platform.twitter.com/widgets.js';
       fjs.parentNode.insertBefore(js,fjs);}}(document, 'script', 'twitter-wjs');
       </script>
       <iframe src="http://ghbtns.com/github-btn.html?user=Edinburgh-Genome-Foundry&repo=caravagene&type=watch&count=true&size=large"
       allowtransparency="true" frameborder="0" scrolling="0" width="152px" height="30px" margin-bottom="30px"></iframe>




.. toctree::
    :hidden:
    :maxdepth: 3

    self
    ref

.. toctree::
   :caption: Examples
   :maxdepth: 1

   examples/construct_jpeg
   examples/multiconstruct
   examples/from_spreadsheet
   examples/from_json



.. _Zulko: https://github.com/Zulko/
.. _Github: https://github.com/EdinburghGenomeFoundry/caravagene
.. _PYPI: https://pypi.python.org/pypi/caravagene
