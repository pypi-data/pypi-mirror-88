from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Bios:
	"""Bios commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("bios", core, parent)

	def get_version(self) -> str:
		"""SYSTem:BIOS:VERSion \n
		Queries the BIOS version of the instrument. \n
			:return: version: string
		"""
		response = self._core.io.query_str('SYSTem:BIOS:VERSion?')
		return trim_str_response(response)
