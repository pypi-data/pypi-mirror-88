from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PpsMarker:
	"""PpsMarker commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ppsMarker", core, parent)

	def get_state(self) -> bool:
		"""[SOURce<HW>]:IQ:OUTPut:[ANALog]:PPSMarker:STATe \n
		No command help available \n
			:return: pps_marker_state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:ANALog:PPSMarker:STATe?')
		return Conversions.str_to_bool(response)
