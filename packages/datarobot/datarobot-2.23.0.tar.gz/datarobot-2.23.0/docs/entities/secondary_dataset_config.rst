.. _secondary_dataset_config:

########################
Secondary Dataset Config
########################
Secondary Dataset Config allows the user to use the different secondary datasets
for Feature Discovery Project during prediction time.

Create Secondary Dataset Configuration
**************************************

Create the secondary dataset configuration for the Feature discovery Project which uses
two secondary datasets profile and transaction.

.. code-block:: python

    import datarobot as dr
    >>> project = dr.Project.get(project_id='54e639a18bd88f08078ca831')


    >>> secondary_datasets = [
        {
            'snapshot_policy': u'latest',
            'identifier': u'profile',
            'catalog_version_id': u'5fd06b4af24c641b68e4d88f',
            'catalog_id': u'5fd06b4af24c641b68e4d88e'
        },
        {
            'snapshot_policy': u'dynamic',
            'identifier': u'transaction',
            'catalog_version_id': u'5fd1e86c589238a4e635e98e',
            'catalog_id': u'5fd1e86c589238a4e635e98d'
        }
    ]
    >>> new_secondary_dataset_config = dr.SecondaryDatasetConfigurations.create(
                                            project_id=project.id,
                                            name='My config',
                                            secondary_datasets=secondary_datasets
                                       )


    >>> new_secondary_dataset_config.id
    '5fd1e86c589238a4e635e93d'

Retrieve Secondary Dataset Config
*********************************

You can retrieve specific secondary dataset configuration using the ID


.. code-block:: python

    >>> config_id = '5fd1e86c589238a4e635e93d

    >>> secondary_dataset_config = dr.SecondaryDatasetConfigurations(id=config_id).get()
    >>> secondary_dataset_config.id == config_id
    True
    >>> secondary_dataset_config
        {
             'created': datetime.datetime(2020, 12, 9, 6, 16, 22, tzinfo=tzutc()),
             'creator_full_name': u'abc@datarobot.com',
             'creator_user_id': u'asdf4af1gf4bdsd2fba1de0a',
             'credential_ids': None,
             'featurelist_id': None,
             'id': u'5fd1e86c589238a4e635e93d',
             'is_default': True,
             'name': u'My config',
             'project_id': u'5fd06afce2456ec1e9d20457',
             'project_version': None,
             'secondary_datasets': [
                    {
                        'snapshot_policy': u'latest',
                        'identifier': u'profile',
                        'catalog_version_id': u'5fd06b4af24c641b68e4d88f',
                        'catalog_id': u'5fd06b4af24c641b68e4d88e'
                    },
                    {
                        'snapshot_policy': u'dynamic',
                        'identifier': u'transaction',
                        'catalog_version_id': u'5fd1e86c589238a4e635e98e',
                        'catalog_id': u'5fd1e86c589238a4e635e98d'
                    }
             ]
        }

List All the Secondary Dataset Config
*************************************

You can list all the secondary dataset configuration created in the project


.. code-block:: python

    >>> secondary_dataset_configs = dr.SecondaryDatasetConfigurations.list(project.id)
    >>> secondary_dataset_configs[0]
        {
             'created': datetime.datetime(2020, 12, 9, 6, 16, 22, tzinfo=tzutc()),
             'creator_full_name': u'abc@datarobot.com',
             'creator_user_id': u'asdf4af1gf4bdsd2fba1de0a',
             'credential_ids': None,
             'featurelist_id': None,
             'id': u'5fd1e86c589238a4e635e93d',
             'is_default': True,
             'name': u'My config',
             'project_id': u'5fd06afce2456ec1e9d20457',
             'project_version': None,
             'secondary_datasets': [
                    {
                        'snapshot_policy': u'latest',
                        'identifier': u'profile',
                        'catalog_version_id': u'5fd06b4af24c641b68e4d88f',
                        'catalog_id': u'5fd06b4af24c641b68e4d88e'
                    },
                    {
                        'snapshot_policy': u'dynamic',
                        'identifier': u'transaction',
                        'catalog_version_id': u'5fd1e86c589238a4e635e98e',
                        'catalog_id': u'5fd1e86c589238a4e635e98d'
                    }
             ]
        }
