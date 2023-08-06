##########
QuickStart
##########

.. note::

    You must set up credentials in order to access the DataRobot API. For more information,
    see :ref:`Credentials<credentials>`

All of the modeling within DataRobot happens within a project. Each project has one dataset that is used as the source from which to train models.

There are three steps required to begin modeling:

1. Create an empty project.
2. Upload a data file to model.
3. Select parameters and start training models with the autopilot.

The following command includes these three steps. It is equivalent to choosing all of the default settings recommended by DataRobot.

.. code-block:: python

    import datarobot as dr
    project = dr.Project.start(project_name='My new project',
                            sourcedata='/home/user/data/last_week_data.csv',
                            target='ItemsPurchased')
                            
Where:

* ``name`` is the name of the new DataRobot project.
* ``sourcedata`` is the path to the dataset.
* ``target`` is the name of the target feature column in the dataset.

You can also pass additional optional parameters:

* ``worker_count`` -- int, sets number of workers used for modeling.
* ``metric`` - str, name of metric to use.
* ``autopilot_on`` - boolean, defaults to ``True``; set whether or not to begin modeling automatically.
* ``blueprint_threshold`` -- int, number of hours the model is permitted to run. Minimum 1.
* ``response_cap`` -- float, Quantile of the response distribution to use for response capping. Must be in range 0.5..1.0
* ``partitioning_method`` -- ``PartitioningMethod`` object.
* ``positive_class`` -- str, float, or int; Specifies a level of the target column that should treated as the positive class for binary classification.  May only be specified for binary classification targets.
* ``target_type`` -- str, override the automaticially selected target_type. An example usage would be setting the `target_type=TARGET_TYPE.MULTICLASS` when you want to perform a multiclass classification task on a numeric column that has a low cardinality.
