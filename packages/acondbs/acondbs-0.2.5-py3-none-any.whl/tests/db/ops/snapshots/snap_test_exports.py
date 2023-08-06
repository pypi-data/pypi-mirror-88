# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import GenericRepr, Snapshot


snapshots = Snapshot()

snapshots['test_export_db_to_dict_of_dict_list 1'] = {
    'admin_app_token': [
        {
            'token': b'aKjGknYDHY39Z2xAaN7+sQ==',
            'token_id': 1
        }
    ],
    'product_file_paths': [
        {
            'note': '',
            'path': 'nersc:/go/to/my/maps',
            'path_id': 1,
            'product_id': 1001
        },
        {
            'note': 'lat only',
            'path': 'nersc:/go/to/my/maps_v2',
            'path_id': 2,
            'product_id': 1012
        },
        {
            'note': 'lat only',
            'path': 'abcde:/path/to/the/maps_v2',
            'path_id': 3,
            'product_id': 1012
        },
        {
            'note': 'lat only',
            'path': 'nersc:/go/to/my/maps_v3',
            'path_id': 4,
            'product_id': 1013
        },
        {
            'note': '',
            'path': 'BEAM_DEPOT/Beams/20190304',
            'path_id': 5,
            'product_id': 1070
        },
        {
            'note': '',
            'path': 'BEAM_DEPOT/Beams/20190607',
            'path_id': 6,
            'product_id': 1120
        },
        {
            'note': '',
            'path': 'BEAM_DEPOT/Beams/20200123',
            'path_id': 7,
            'product_id': 1130
        },
        {
            'note': '',
            'path': 'BEAM_DEPOT/Beams/20200207',
            'path_id': 8,
            'product_id': 1150
        },
        {
            'note': '',
            'path': 'nersc:/go/to/my/simulations',
            'path_id': 9,
            'product_id': 1002
        },
        {
            'note': '',
            'path': 'abcde:/path/to/the/simulations',
            'path_id': 10,
            'product_id': 1002
        }
    ],
    'product_relation_types': [
        {
            'indef_article': 'a',
            'name': 'parent',
            'plural': 'parents',
            'reverse_type_id': 2,
            'singular': 'parent',
            'type_id': 1
        },
        {
            'indef_article': 'a',
            'name': 'child',
            'plural': 'children',
            'reverse_type_id': 1,
            'singular': 'child',
            'type_id': 2
        },
        {
            'indef_article': 'a',
            'name': 'plaintiff',
            'plural': 'plaintiffs',
            'reverse_type_id': 4,
            'singular': 'plaintiff',
            'type_id': 3
        },
        {
            'indef_article': 'a',
            'name': 'defendant',
            'plural': 'defendants',
            'reverse_type_id': 3,
            'singular': 'defendant',
            'type_id': 4
        }
    ],
    'product_relations': [
        {
            'other_product_id': 1012,
            'relation_id': 1,
            'reverse_relation_id': 2,
            'self_product_id': 1130,
            'type_id': 1
        },
        {
            'other_product_id': 1130,
            'relation_id': 2,
            'reverse_relation_id': 1,
            'self_product_id': 1012,
            'type_id': 2
        },
        {
            'other_product_id': 1013,
            'relation_id': 3,
            'reverse_relation_id': 4,
            'self_product_id': 1150,
            'type_id': 1
        },
        {
            'other_product_id': 1150,
            'relation_id': 4,
            'reverse_relation_id': 3,
            'self_product_id': 1013,
            'type_id': 2
        },
        {
            'other_product_id': 1130,
            'relation_id': 5,
            'reverse_relation_id': 6,
            'self_product_id': 1150,
            'type_id': 1
        },
        {
            'other_product_id': 1150,
            'relation_id': 6,
            'reverse_relation_id': 5,
            'self_product_id': 1130,
            'type_id': 2
        }
    ],
    'product_types': [
        {
            'icon': 'mdi-map',
            'indef_article': 'a',
            'name': 'map',
            'order': 2,
            'plural': 'maps',
            'singular': 'map',
            'type_id': 1
        },
        {
            'icon': 'mdi-spotlight-beam',
            'indef_article': 'a',
            'name': 'beam',
            'order': 3,
            'plural': 'beams',
            'singular': 'beam',
            'type_id': 2
        },
        {
            'icon': 'mdi-creation',
            'indef_article': 'a',
            'name': 'simulation',
            'order': 1,
            'plural': 'simulations',
            'singular': 'simulation',
            'type_id': 3
        },
        {
            'icon': '',
            'indef_article': '',
            'name': 'anchor',
            'order': 4,
            'plural': '',
            'singular': '',
            'type_id': 4
        }
    ],
    'products': [
        {
            'contact': 'pwg-pmn',
            'date_posted': GenericRepr('datetime.date(2019, 2, 13)'),
            'date_produced': GenericRepr('datetime.date(2019, 2, 13)'),
            'date_updated': GenericRepr('datetime.date(2019, 2, 13)'),
            'name': 'lat20190213',
            'note': '''- This is a dummy test with a lat map
- This should not depend on any beam''',
            'posted_by': 'pwg-pmn',
            'produced_by': 'pwg-pmn',
            'product_id': 1001,
            'type_id': 1,
            'updated_by': 'pwg-pmn'
        },
        {
            'contact': 'abc-def',
            'date_posted': GenericRepr('datetime.date(2019, 3, 15)'),
            'date_produced': GenericRepr('datetime.date(2019, 3, 15)'),
            'date_updated': None,
            'name': 'xyz-s1234-20200101',
            'note': '''- note 1
- note 2''',
            'posted_by': 'abc-def',
            'produced_by': 'abc-def',
            'product_id': 1002,
            'type_id': 3,
            'updated_by': ''
        },
        {
            'contact': 'pwg-pmn',
            'date_posted': GenericRepr('datetime.date(2018, 1, 1)'),
            'date_produced': GenericRepr('datetime.date(2018, 1, 1)'),
            'date_updated': None,
            'name': '20180101',
            'note': '- test entry',
            'posted_by': 'pwg-pmn',
            'produced_by': 'pwg-pmn',
            'product_id': 1010,
            'type_id': 2,
            'updated_by': ''
        },
        {
            'contact': 'pwg-pmn',
            'date_posted': GenericRepr('datetime.date(2020, 1, 20)'),
            'date_produced': GenericRepr('datetime.date(2020, 1, 20)'),
            'date_updated': GenericRepr('datetime.date(2020, 1, 20)'),
            'name': 'lat20200120',
            'note': '''- This is a dummy test with a lat map
- A beam depends on this map''',
            'posted_by': 'pwg-pmn',
            'produced_by': 'pwg-pmn',
            'product_id': 1012,
            'type_id': 1,
            'updated_by': 'pwg-pmn'
        },
        {
            'contact': 'pwg-pmn',
            'date_posted': GenericRepr('datetime.date(2020, 2, 1)'),
            'date_produced': GenericRepr('datetime.date(2020, 2, 1)'),
            'date_updated': GenericRepr('datetime.date(2020, 2, 1)'),
            'name': 'lat20200201',
            'note': '''- This is a dummy test with a lat map
- A beam depends on this map''',
            'posted_by': 'pwg-pmn',
            'produced_by': 'pwg-pmn',
            'product_id': 1013,
            'type_id': 1,
            'updated_by': 'pwg-pmn'
        },
        {
            'contact': 'pwg-pmn',
            'date_posted': GenericRepr('datetime.date(2019, 3, 4)'),
            'date_produced': GenericRepr('datetime.date(2019, 3, 4)'),
            'date_updated': None,
            'name': '20190304',
            'note': '- test entry',
            'posted_by': 'pwg-pmn',
            'produced_by': 'pwg-pmn',
            'product_id': 1070,
            'type_id': 2,
            'updated_by': ''
        },
        {
            'contact': 'pwg-pmn',
            'date_posted': GenericRepr('datetime.date(2019, 6, 7)'),
            'date_produced': GenericRepr('datetime.date(2019, 6, 7)'),
            'date_updated': None,
            'name': '20190607',
            'note': '- test entry',
            'posted_by': 'pwg-pmn',
            'produced_by': 'pwg-pmn',
            'product_id': 1120,
            'type_id': 2,
            'updated_by': ''
        },
        {
            'contact': 'pwg-pmn',
            'date_posted': GenericRepr('datetime.date(2020, 1, 23)'),
            'date_produced': GenericRepr('datetime.date(2020, 1, 23)'),
            'date_updated': None,
            'name': '20200123',
            'note': '- test entry',
            'posted_by': 'pwg-pmn',
            'produced_by': 'pwg-pmn',
            'product_id': 1130,
            'type_id': 2,
            'updated_by': ''
        },
        {
            'contact': 'pwg-pmn',
            'date_posted': GenericRepr('datetime.date(2020, 2, 7)'),
            'date_produced': GenericRepr('datetime.date(2020, 2, 7)'),
            'date_updated': None,
            'name': '20200207',
            'note': '- test entry',
            'posted_by': 'pwg-pmn',
            'produced_by': 'pwg-pmn',
            'product_id': 1150,
            'type_id': 2,
            'updated_by': ''
        }
    ],
    'web_config': [
        {
            'config_id': 1,
            'devtool_loadingstate': True,
            'head_title': 'Product DB (test)',
            'product_creation_dialog': True,
            'product_deletion_dialog': False,
            'product_update_dialog': True,
            'toolbar_title': 'Product DB (test)'
        }
    ]
}
