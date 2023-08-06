from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class GuiFramework:
	"""GuiFramework commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("guiFramework", core, parent)

	def get_version(self) -> str:
		"""SYSTem:PACKage:GUIFramework:VERSion \n
		No command help available \n
			:return: version: No help available
		"""
		response = self._core.io.query_str('SYSTem:PACKage:GUIFramework:VERSion?')
		return trim_str_response(response)
