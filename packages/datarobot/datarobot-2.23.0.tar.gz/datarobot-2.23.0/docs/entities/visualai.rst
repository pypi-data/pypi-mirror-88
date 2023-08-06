.. _visualai:

##################
Visual AI Projects
##################

With Visual AI, DataRobot allows you to use image data for modeling. You can create projects with one
or multiple image features and also mix them with other DataRobot-supported feature types. You can
find more information about
`Visual AI <https://app.datarobot.com/docs/modeling/visual-ai/index.html>`_
in the Platform documentation.


Create a Visual AI Project
**************************

DataRobot offers you different ways to prepare your dataset and to start a Visual AI project. The
various ways to do this are covered in detail in the documentation,
`Preparing the dataset <https://app.datarobot.com/docs/modeling/visual-ai/vai-model.html>`_.

For the examples given here the images are partitioned into named
directories. In the following, images are partitioned into named directories, which serve as labels
for the project. For example, to predict on images of cat and dog breeds, labels could be
abyssinian, american_bulldog, etc.

::

    /home/user/data/imagedataset
        ├── abyssinian
        │   ├── abyssinian01.jpg
        │   ├── abyssinian02.jpg
        │   ├── …
        ├── american_bulldog
        │   ├── american_bulldog01.jpg
        │   ├── american_bulldog02.jpg
        │   ├── …


You then compress the directory containing the named directories into a
ZIP file, creating the dataset used for the project.

.. code-block:: python

    from datarobot.models import Project, Dataset
    dataset = Dataset.create_from_file(file_path='/home/user/data/imagedataset.zip')
    project = Project.create_from_dataset(dataset.id, project_name='My Image Project')


Target
======

Since this example uses named directories the target name must be
``class``, which will contain the name of each directory in the ZIP
file. 



Other Parameters
================

Setting modeling parameters, such as partitioning method, queue mode,
etc, functions in the same way as starting a non-image project.



Start Modeling
**************

Once you have set modeling parameters, use the following code snippet
to specify parameters and start the modeling process.

.. code-block:: python

    from datarobot import AUTOPILOT_MODE
    project.set_target(target='class', mode=AUTOPILOT_MODE.QUICK)


You can also pass optional parameters to ``project.set_target``
to change aspects of the modeling process. Some of those parameters
include:

* ``worker_count`` -- int, sets the number of workers used for modeling.

* ``partitioning_method`` -- ``PartitioningMethod`` object.


For a full reference of available parameters, see
:meth:`Project.set_target <datarobot.models.Project.set_target>`.

You can use the ``mode`` parameter to set the Autopilot mode.
``AUTOPILOT_MODE.FULL_AUTO``, is the default, triggers modeling
with no further actions necessary. Other accepted modes include
``AUTOPILOT_MODE.MANUAL`` for manual mode (choose your own models to run
rather than running the full Autopilot) and ``AUTOPILOT_MODE.QUICK`` to
run on a more limited set of models and get insights more quickly
("quick run").



Interact with a Visual AI Project
*********************************

The following code snippets may be used to access Visual AI images and
insights.



List Sample Images
==================

Sample images allow you to see a subset of images, chosen by DataRobot,
in the dataset. The returned ``SampleImage`` objects have an associated
``target_value`` that will allow you to categorize the images (abyssinian, american_bulldog, etc).
Until you set the target and EDA2 has finished, the ``target_value`` will be ``None``.


.. code-block:: python
	
    import io
    import PIL.Image

    from datarobot.models.visualai import SampleImage

    column_name = "image"
    number_of_images_to_show = 5

    for sample in SampleImage.list(project.id, column_name)[:number_of_images_to_show]:
        # Display the image in the GUI
        bio = io.BytesIO(sample.image.image_bytes)
        img = PIL.Image.open(bio)
        img.show()

The results would be images such as:

.. image:: images/visualai/sample1.png

.. image:: images/visualai/sample2.png


List Duplicate Images
=====================

Duplicate images, images with different names but are determined by DataRobot
to be the same, may exist in a dataset. If this happens, the code returns
one of the images and the number of times it occurs in the dataset.

.. code-block:: python
	
    from datarobot.models.visualai import DuplicateImage

    column_name = "image"

    for duplicate in DuplicateImage.list(project.id, column_name):
        # To show an image see the previous sample image example
        print(f"Image id = {duplicate.image.id} has {duplicate.count} duplicates")


Activation Maps
===============

Activation maps are overlaid on the images to show which image areas are driving model prediction
decisions.

Detailed explanations are available in DataRobot Platform
documentation, `Model insights <https://app.datarobot.com/docs/modeling/visual-ai/vai-insights.html>`_.


Compute Activation Maps
-----------------------

To begin, you must first compute activation maps. The following snippet is an example of starting
the computation for a Keras model in a Visual AI project. The ``compute`` method returns a URL that
can be used to determine when the computation completes.

.. code-block:: python

    from datarobot.models.visualai import ImageActivationMap

    keras_model = project.get_models(search_params={'name': 'Keras'})[0]

    status_url = ImageActivationMap.compute(project.id, keras_model.id)
    print(status_url)


List Activation Maps
--------------------

After activation maps are computed, you can download them from the
DataRobot server. The following snippet is an example of how to get the
activation maps and how to plot them.


.. code-block:: python

    import PIL.Image
    from datarobot.models.visualai import ImageActivationMap

    column_name = "image"
    max_activation_maps = 5
    keras_model = project.get_models(search_params={'name': 'Keras'})[0]

    for activation_map in ImageActivationMap.list(project.id, keras_model.id, column_name)[:max_activation_maps]:
        bio = io.BytesIO(activation_map.overlay_image.image_bytes)
        img = PIL.Image.open(bio)
        img.show()


.. image:: images/visualai/activation_map1.png

.. image:: images/visualai/activation_map2.png



Image Embeddings
================

Image embeddings allow you to get an impression on how similar two images look to a featurizer
network. The embeddings project images from their high-dimensional feature space onto a 2D plane.
The closer the images appear in this plane, the more similar they look to the featurizer.

Detailed explanations are available in the DataRobot Platform documentation,
`Model insights <https://app.datarobot.com/docs/modeling/visual-ai/vai-insights.html>`_.


Compute Image Embeddings
------------------------

You must compute image embeddings before retrieving. The following snippet
is an example of starting the computation for a Keras model in our Visual AI project. The
``compute`` method returns a URL that can be used to determine when the computation is complete.

.. code-block:: python

    from datarobot.models.visualai import ImageEmbedding

    keras_model = project.get_models(search_params={'name': 'Keras'})[0]

    status_url = ImageEmbedding.compute(project.id, keras_model.id)
    print(status_url)


List Image Embeddings
---------------------

After image embeddings are computed, you can download them from the
DataRobot server. The following snippet is an example of how to get the
embeddings for a model and plot them.

.. code-block:: python

    from matplotlib.offsetbox import OffsetImage, AnnotationBbox
    import matplotlib.pyplot as plt
    import numpy as np
    import PIL.Image

    from datarobot.models.visualai import ImageEmbedding

    column_name = "image"
    keras_model = project.get_models(search_params={'name': 'Keras'})[0]
    zoom = 0.15

    fig, ax = plt.subplots(figsize=(15,10))
    for image_embedding in ImageEmbedding.list(project.id, keras_model.id, column_name):
        image_bytes = image_embedding.image.image_bytes
        x_position = image_embedding.position_x
        y_position = image_embedding.position_y
        image = PIL.Image.open(io.BytesIO(image_bytes))
        offset_image = OffsetImage(np.array(image), zoom=zoom)
        annotation_box = AnnotationBbox(offset_image, (x_position, y_position), xycoords='data', frameon=False)
        ax.add_artist(annotation_box)
        ax.update_datalim([(x_position, y_position)])
    ax.autoscale()
    ax.grid(True)
    fig.show()
.. image:: images/visualai/embeddings.png

License
=======
For the examples here we used the
`The Oxford-IIIT Pet Dataset <https://www.robots.ox.ac.uk/~vgg/data/pets/>`_ licensed under
`Creative Commons Attribution-ShareAlike 4.0 International License <https://creativecommons.org/licenses/by-sa/4.0/>`_
