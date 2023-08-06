from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Coupling:
	"""Coupling commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("coupling", core, parent)

	def get_state(self) -> bool:
		"""[SOURce<HW>]:AWGN:BWIDth:COUPling:[STATe] \n
		No command help available \n
			:return: awgn_bw_coup_state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AWGN:BWIDth:COUPling:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, awgn_bw_coup_state: bool) -> None:
		"""[SOURce<HW>]:AWGN:BWIDth:COUPling:[STATe] \n
		No command help available \n
			:param awgn_bw_coup_state: No help available
		"""
		param = Conversions.bool_to_str(awgn_bw_coup_state)
		self._core.io.write(f'SOURce<HwInstance>:AWGN:BWIDth:COUPling:STATe {param}')
