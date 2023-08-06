from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Frequency:
	"""Frequency commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("frequency", core, parent)

	def get_sw_points(self) -> str:
		"""CALibration:FREQuency:SWPoints \n
		No command help available \n
			:return: freq_switch_point: No help available
		"""
		response = self._core.io.query_str('CALibration:FREQuency:SWPoints?')
		return trim_str_response(response)

	def set_sw_points(self, freq_switch_point: str) -> None:
		"""CALibration:FREQuency:SWPoints \n
		No command help available \n
			:param freq_switch_point: No help available
		"""
		param = Conversions.value_to_quoted_str(freq_switch_point)
		self._core.io.write(f'CALibration:FREQuency:SWPoints {param}')

	def get_measure(self) -> bool:
		"""CALibration<HW>:FREQuency:[MEASure] \n
		No command help available \n
			:return: measure: No help available
		"""
		response = self._core.io.query_str('CALibration<HwInstance>:FREQuency:MEASure?')
		return Conversions.str_to_bool(response)
