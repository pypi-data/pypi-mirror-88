from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Exchange:
	"""Exchange commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("exchange", core, parent)

	def get_xml_string(self) -> str:
		"""[SOURce<HW>]:BB:NR5G:SETTing:EXCHange:XMLString \n
		No command help available \n
			:return: set_exch_xml_str: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:SETTing:EXCHange:XMLString?')
		return trim_str_response(response)
