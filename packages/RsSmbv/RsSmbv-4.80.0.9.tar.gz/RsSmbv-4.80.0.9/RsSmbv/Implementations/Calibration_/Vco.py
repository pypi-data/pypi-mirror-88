from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Vco:
	"""Vco commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("vco", core, parent)

	def get_limits(self) -> str:
		"""CALibration:VCO:LIMits \n
		No command help available \n
			:return: vco_limits: No help available
		"""
		response = self._core.io.query_str('CALibration:VCO:LIMits?')
		return trim_str_response(response)
