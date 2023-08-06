import datajoint as dj
import os
dj.config['enable_python_native_blobs'] = True

reference = dj.create_virtual_module('reference', 'ibl_reference')
subject = dj.create_virtual_module('subject', 'ibl_subject')
action = dj.create_virtual_module('action', 'ibl_action')
acquisition = dj.create_virtual_module('acquisition', 'ibl_acquisition')
data = dj.create_virtual_module('data', 'ibl_data')
behavior = dj.create_virtual_module('behavior', 'ibl_behavior')
behavior_analyses = dj.create_virtual_module('behavior_analyses', 'ibl_analyses_behavior')

accessible_schemas = dj.list_schemas()

if 'ibl_ephys' in accessible_schemas and \
        'ibl_storage' in accessible_schemas:

    schema = dj.schema('ibl_storage')

    @schema
    class S3Access(dj.Manual):
        definition = """
        s3_id:  tinyint   # unique id for each S3 pair
        ---
        access_key: varchar(128)   # S3 access key
        secret_key: varchar(128)   # S3 secret key
        """

    # attempt to get S3 access/secret key from different sources
    access_key = os.environ.get('S3_ACCESS')
    secret_key = os.environ.get('S3_SECRET')

    if (access_key is None or secret_key is None) and S3Access():
        # if there are multiple entries in S3, it won't work
        access_key, secret_key = S3Access.fetch1('access_key', 'secret_key')

    dj.config['stores'] = {
        'ephys': dict(
            protocol='s3',
            endpoint='s3.amazonaws.com',
            access_key=access_key,
            secret_key=secret_key,
            bucket='ibl-dj-external',
            location='/ephys'
        )
    }

    ephys = dj.create_virtual_module('ephys', 'ibl_ephys')

    if 'ibl_histology' in accessible_schemas:
        histology = dj.create_virtual_module('histology', 'ibl_histology')

        if 'ibl_qc' in accessible_schemas:
            qc = dj.create_virtual_module('qc', 'ibl_qc')
