.. _reference:

Caravagene Reference manual
==========================

.. mermaid::
   :align: center

   graph LR;
    param1(category) --> Part
    param2(label) --> Part
    param3(name) --> Construct
    param4(note) --> Construct
    param5(name) --> ConstructList
    param6(note) --> ConstructList
    Part --> Construct
    Part --> Construct
    Part --> Construct
    Construct --> ConstructList
    Construct --> ConstructList
    Construct --> ConstructList
    style param1 fill:none,stroke:none;
    style param2 fill:none,stroke:none;
    style param3 fill:none,stroke:none;
    style param4 fill:none,stroke:none;
    style param5 fill:none,stroke:none;
    style param6 fill:none,stroke:none;

.. autoclass:: caravagene.Part
   :members:


.. autoclass:: caravagene.Construct
  :members:


.. autoclass:: caravagene.ConstructList
   :members:
