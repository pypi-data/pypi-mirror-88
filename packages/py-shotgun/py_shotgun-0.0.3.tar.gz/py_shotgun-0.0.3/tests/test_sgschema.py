import os
import sys
import datetime
import unittest

from shotgun_api3 import Shotgun
import py_shotgun

url = r'https://{}.shotgunstudio.com'.format(os.environ['SHOTGUNSTUDIO'])
script_name = os.environ['script_name']
api_key = os.environ['PYSHOTGUNAPI']

sg = Shotgun(
    url,
    script_name=script_name,
    api_key=api_key)


class TestSgschema(unittest.TestCase):
    def setUp(self):
        import logging
        self.logger = logging.getLogger(__file__)
        self.logger.setLevel(logging.DEBUG)
        self.asset1 = {'id':1406, 'name':"Wepon01", 'type':'Asset'}
        self.event_log1 = {'attribute_name': 'sg_status_list',
                           'cached_display_name': None,
                           'created_at': datetime.datetime(2020, 12, 13, 17, 30, 55),
                           'description': 'David Lin changed "Status" from "rev" to "apr" on Version '
                           'v076_seq004_sh0010_Comp',
                           'entity': {'id': 19613, 'name': 'v076_seq004_sh0010_Comp', 'type': 'Version'},
                           'event_type': 'Shotgun_Version_Change',
                           'filmstrip_image': None,
                           'id': 2282801,
                           'image': None,
                           'image_blur_hash': None,
                           'image_source_entity': None,
                           'meta': {'attribute_name': 'sg_status_list',
                                    'entity_id': 19613,
                                    'entity_type': 'Version',
                                    'field_data_type': 'status_list',
                                    'new_value': 'apr',
                                    'old_value': 'rev',
                                    'type': 'attribute_change'},
                           'project': {'id': 91, 'name': 'Noflame_Test', 'type': 'Project'},
                           'session_uuid': 'd8aa7698-3d25-11eb-a9d3-0242ac110002',
                           'type': 'EventLogEntry',
                           'user': {'id': 88, 'name': 'David Lin', 'type': 'HumanUser'}}

    def test_sgschema_create(self):
        SGSchema = py_shotgun.SGSchema
        SGSchema.set_api(sg)

        Version = SGSchema.sgClasses.Version
        ver = Version(self.event_log1['entity']['id'], sg, self.logger)
        self.assertTrue(ver)

    def test_name_attribute(self):
        SGSchema = py_shotgun.SGSchema
        SGSchema.set_api(sg)
        Asset = SGSchema.sgClasses.Asset
        Version = SGSchema.sgClasses.Version
        ver = Version(self.event_log1['entity']['id'], sg, self.logger)
        print(ver.name_())
        ast = Asset(self.asset1['id'], sg, self.logger)
        print(ast.name_())

