from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Startup:
	"""Startup commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("startup", core, parent)

	def get_complete(self) -> bool:
		"""SYSTem:STARtup:COMPlete \n
		Queries if the startup of the instrument is completed. \n
			:return: complete: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SYSTem:STARtup:COMPlete?')
		return Conversions.str_to_bool(response)
