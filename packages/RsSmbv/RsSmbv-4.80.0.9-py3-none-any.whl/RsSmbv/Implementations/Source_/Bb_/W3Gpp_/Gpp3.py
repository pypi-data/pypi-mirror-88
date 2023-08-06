from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Gpp3:
	"""Gpp3 commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("gpp3", core, parent)

	def get_version(self) -> str:
		"""[SOURce]:BB:W3GPp:GPP3:VERSion \n
		The command queries the version of the 3GPP standard underlying the definitions. \n
			:return: version: string
		"""
		response = self._core.io.query_str('SOURce:BB:W3GPp:GPP3:VERSion?')
		return trim_str_response(response)
