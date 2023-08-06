import json
import os

from itsimodels.core.field_decode import BackupFieldDecoder
from itsimodels.correlation_search import *
from itsimodels.deep_dive import *
from itsimodels.entity_type import *
from itsimodels.glass_table import *
from itsimodels.glass_table_icon import *
from itsimodels.glass_table_image import *
from itsimodels.kpi_base_search import *
from itsimodels.kpi_threshold_template import *
from itsimodels.neap import *
from itsimodels.service import *
from itsimodels.service_analyzer import *
from itsimodels.service_template import *
from itsimodels.team import *


HERE = os.path.dirname(os.path.realpath(__file__))


def test_service_model():
	fixture = os.path.join(HERE, 'fixtures', 'backup', 'services.json')

	with open(fixture) as fobj:
		raw_objects = json.loads(fobj.read())

	objects = []
	for raw_data in raw_objects:
		decoded = Service(raw_data, field_decoder=BackupFieldDecoder())
		objects.append(decoded)

	assert len(objects) == 36

	for model in objects:
		raw_data = model.to_dict()

		service = Service(raw_data)

		backup = model.to_dict(use_alias=True)
