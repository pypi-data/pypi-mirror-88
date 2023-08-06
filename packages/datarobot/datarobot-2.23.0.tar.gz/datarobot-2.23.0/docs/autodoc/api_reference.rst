API Reference
#############

.. _advanced_options_api:

Advanced Options
================

.. autoclass:: datarobot.helpers.AdvancedOptions
   :members:

.. _batch_prediction_api:

Batch Predictions
=================

.. autoclass:: datarobot.models.BatchPredictionJob
   :members:

Blueprint
=========

.. autoclass:: datarobot.models.Blueprint
   :members:

.. autoclass:: datarobot.models.BlueprintTaskDocument
   :members:

.. autoclass:: datarobot.models.BlueprintChart
   :members:

.. autoclass:: datarobot.models.ModelBlueprintChart
   :members: get, to_graphviz

Calendar File
=============

.. autoclass:: datarobot.CalendarFile
   :members:

Compliance Documentation Templates
==================================

.. autoclass:: datarobot.models.compliance_doc_template.ComplianceDocTemplate
   :members:

Compliance Documentation
========================

.. autoclass:: datarobot.models.compliance_documentation.ComplianceDocumentation
   :members:

Confusion Chart
===============

.. autoclass:: datarobot.models.confusion_chart.ConfusionChart
   :members:

.. _credential_api:

Credentials
=================

.. autoclass:: datarobot.models.Credential
   :members:

Custom Models
=============

.. autoclass:: datarobot.models.custom_model_version.CustomModelFileItem
   :members:

.. autoclass:: datarobot.CustomInferenceImage
   :members:

.. autoclass:: datarobot.CustomInferenceModel
   :members:

.. autoclass:: datarobot.CustomModelTest
   :members:

.. autoclass:: datarobot.CustomModelVersion
   :members:

.. autoclass:: datarobot.CustomModelVersionDependencyBuild
   :members:

.. autoclass:: datarobot.ExecutionEnvironment
   :members:

.. autoclass:: datarobot.ExecutionEnvironmentVersion
   :members:

Database Connectivity
=====================

.. autoclass:: datarobot.DataDriver
   :members:

.. autoclass:: datarobot.DataStore
   :members:

.. autoclass:: datarobot.DataSource
   :members:

.. autoclass:: datarobot.DataSourceParameters

Datasets
========

.. autoclass:: datarobot.Dataset
   :members:

.. autoclass:: datarobot.DatasetDetails
   :members:

Deployment
==========

.. autoclass:: datarobot.Deployment
   :members:

.. autoclass:: datarobot.models.deployment.DeploymentListFilters
   :members:

.. autoclass:: datarobot.models.ServiceStats
   :members:

.. autoclass:: datarobot.models.ServiceStatsOverTime
   :members:

.. autoclass:: datarobot.models.TargetDrift
   :members:

.. autoclass:: datarobot.models.FeatureDrift
   :members:

.. autoclass:: datarobot.models.Accuracy
   :members:

.. autoclass:: datarobot.models.AccuracyOverTime
   :members:

External Scores and Insights
============================

.. autoclass:: datarobot.ExternalScores
   :members:

.. autoclass:: datarobot.ExternalLiftChart
   :members:

.. autoclass:: datarobot.ExternalRocCurve
   :members:

Feature
=======

.. autoclass:: datarobot.models.Feature
   :members:

.. autoclass:: datarobot.models.ModelingFeature
   :members:

.. autoclass:: datarobot.models.DatasetFeature
   :members:

.. autoclass:: datarobot.models.DatasetFeatureHistogram
   :members:

.. autoclass:: datarobot.models.FeatureHistogram
   :members:

.. autoclass:: datarobot.models.InteractionFeature
   :members:


Feature List
============

.. autoclass:: datarobot.DatasetFeaturelist
   :members: get, update, delete

.. autoclass:: datarobot.models.Featurelist
   :members: get, update, delete

.. autoclass:: datarobot.models.ModelingFeaturelist
   :members: get, update, delete

Job
===

.. _jobs_api:

.. autoclass:: datarobot.models.Job
   :members:
   :inherited-members:

.. autoclass:: datarobot.models.TrainingPredictionsJob
   :members:
   :inherited-members:

.. autoclass:: datarobot.models.ShapMatrixJob
   :members:
   :inherited-members:

.. autoclass:: datarobot.models.FeatureImpactJob
   :members:
   :inherited-members:

Lift Chart
==========

.. autoclass:: datarobot.models.lift_chart.LiftChart
   :members:

.. _missing_values_report_api:

Missing Values Report
=====================

.. autoclass:: datarobot.models.missing_report.MissingValuesReport
   :members:
   :exclude-members: from_server_data

Models
======

Model
*****

.. autoclass:: datarobot.models.Model
   :members:
   :exclude-members: from_server_data

PrimeModel
**********

.. autoclass:: datarobot.models.PrimeModel
   :inherited-members:
   :members:
   :exclude-members: from_server_data, request_frozen_model, request_frozen_datetime_model, train, train_datetime, request_approximation

BlenderModel
************

.. autoclass:: datarobot.models.BlenderModel
   :members:
   :inherited-members:
   :exclude-members: from_server_data

.. _datetime_mod:

DatetimeModel
*************

.. autoclass:: datarobot.models.DatetimeModel
   :inherited-members:
   :members:
   :exclude-members: from_server_data, train, request_frozen_model

Frozen Model
************

.. autoclass:: datarobot.models.FrozenModel
   :members:

Imported Model
**************

.. note::
   Imported Models are used in Stand Alone Scoring Engines.  If you are not an administrator of such
   an engine, they are not relevant to you.

.. autoclass:: datarobot.models.ImportedModel
   :members:

RatingTableModel
****************

.. autoclass:: datarobot.models.RatingTableModel
   :inherited-members:
   :members:
   :exclude-members: from_server_data

Advanced Tuning
***************

.. autoclass:: datarobot.models.advanced_tuning.AdvancedTuningSession
   :members:

ModelJob
========

.. _wait_for_async_model_creation-api-label:
.. autofunction:: datarobot.models.modeljob.wait_for_async_model_creation

.. _modeljob_api:
.. autoclass:: datarobot.models.ModelJob
   :members:
   :inherited-members:

Pareto Front
============

.. autoclass:: datarobot.models.pareto_front.ParetoFront
   :members:

.. autoclass:: datarobot.models.pareto_front.Solution
   :members:

.. _partitions_api:

Partitioning
============

.. autoclass:: datarobot.RandomCV
   :members:

.. autoclass:: datarobot.StratifiedCV
   :members:

.. autoclass:: datarobot.GroupCV
   :members:

.. autoclass:: datarobot.UserCV
   :members:

.. autoclass:: datarobot.RandomTVH
   :members:

.. autoclass:: datarobot.UserTVH
   :members:

.. autoclass:: datarobot.StratifiedTVH
   :members:

.. autoclass:: datarobot.GroupTVH
   :members:

.. _datetime_part_spec:
.. autoclass:: datarobot.DatetimePartitioningSpecification
   :members:

.. autoclass:: datarobot.BacktestSpecification
   :members:

.. autoclass:: datarobot.FeatureSettings
   :members:

.. autoclass:: datarobot.Periodicity
   :members:

.. _datetime_part:
.. autoclass:: datarobot.DatetimePartitioning
   :members:

.. autoclass:: datarobot.helpers.partitioning_methods.Backtest
   :members:

.. _dur_string_helper:
.. autofunction:: datarobot.helpers.partitioning_methods.construct_duration_string

PayoffMatrix
============

.. autoclass:: datarobot.models.PayoffMatrix
   :members:
   :inherited-members:

PredictJob
==========

.. _wait_for_async_predictions=api=label:
.. autofunction:: datarobot.models.predict_job.wait_for_async_predictions

.. _predict_job_api:
.. autoclass:: datarobot.models.PredictJob
   :members:
   :inherited-members:

Prediction Dataset
==================

.. autoclass:: datarobot.models.PredictionDataset
   :members:


.. _pred_expl_api:

Prediction Explanations
=======================

.. autoclass:: datarobot.PredictionExplanationsInitialization
   :members:

.. autoclass:: datarobot.PredictionExplanations
   :members:

.. autoclass:: datarobot.models.prediction_explanations.PredictionExplanationsRow
   :members:

.. autoclass:: datarobot.models.prediction_explanations.PredictionExplanationsPage
   :members:

.. autoclass:: datarobot.models.ShapMatrix
   :members:


.. _predictions_api:

Predictions
===========

.. autoclass:: datarobot.models.Predictions
    :members:

PredictionServer
================

.. autoclass:: datarobot.PredictionServer
    :members:

Ruleset
=======

.. autoclass:: datarobot.models.Ruleset
   :members:

PrimeFile
=========

.. autoclass:: datarobot.models.PrimeFile
   :members:

Project
=======

.. autoclass:: datarobot.models.Project
   :members:

.. autoclass:: datarobot.helpers.eligibility_result.EligibilityResult
   :members:

VisualAI
========

.. autoclass:: datarobot.models.visualai.Image
   :members:

.. autoclass:: datarobot.models.visualai.SampleImage
   :members:

.. autoclass:: datarobot.models.visualai.DuplicateImage
   :members:

.. autoclass:: datarobot.models.visualai.ImageEmbedding
   :members:

.. autoclass:: datarobot.models.visualai.ImageActivationMap
   :members:

Feature Association
===================

.. autoclass:: datarobot.models.feature_association.FeatureAssociation
  :members:

Feature Association Matrix Details
==================================

.. autoclass:: datarobot.models.feature_association.FeatureAssociationMatrixDetails
  :members:

Feature Association Featurelists
================================

.. autoclass:: datarobot.models.feature_association.FeatureAssociationFeaturelists
  :members:


Rating Table
============

.. autoclass:: datarobot.models.RatingTable
   :members:
   :exclude-members: from_server_data

.. _reason_codes_api:

Reason Codes (Deprecated)
=========================

This interface is considered deprecated.  Please use :ref:`PredictionExplanations <pred_expl_api>`
instead.

.. autoclass:: datarobot.ReasonCodesInitialization
   :members:

.. autoclass:: datarobot.ReasonCodes
   :members:

.. autoclass:: datarobot.models.reason_codes.ReasonCodesRow
   :members:

.. autoclass:: datarobot.models.reason_codes.ReasonCodesPage
   :members:


.. _recommended_models:

Recommended Models
==================

.. autoclass:: datarobot.models.ModelRecommendation
   :members:

ROC Curve
=========

.. autoclass:: datarobot.models.roc_curve.RocCurve
   :members:

SharingAccess
=============

.. autoclass:: datarobot.SharingAccess

.. _training_predictions_api:

Training Predictions
====================

.. automodule:: datarobot.models.training_predictions
    :members: TrainingPredictions, TrainingPredictionsIterator

Word Cloud
==========

.. autoclass:: datarobot.models.word_cloud.WordCloud
   :members:

Feature Discovery
=================

.. autoclass:: datarobot.models.SecondaryDatasetConfigurations
   :members: create, get, delete, list

.. autoclass:: datarobot.models.RelationshipsConfiguration
   :members: create, get, delete, replace

.. autoclass:: datarobot.models.FeatureLineage
   :members: get

SHAP
====

.. autoclass:: datarobot.models.ShapImpact
   :members:
