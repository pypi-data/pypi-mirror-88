from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Load:
	"""Load commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("load", core, parent)

	def set_predefined(self, scenario: str) -> None:
		"""[SOURce<HW>]:BB:GNSS:SETTing:LOAD:PREDefined \n
		Loads the selected scenario file. \n
			:param scenario: 'ScenarioName' Name of a predefined scenario, as queried with the command method RsSmbv.Source.Bb.Gnss.Setting.Catalog.predefined.
		"""
		param = Conversions.value_to_quoted_str(scenario)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SETTing:LOAD:PREDefined {param}')
