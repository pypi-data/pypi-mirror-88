from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mcs:
	"""Mcs commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mcs", core, parent)

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:HUWB:FCONfig:MCS:STATe \n
		Activates MAC frame check sequence field. \n
			:return: mcs_state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:FCONfig:MCS:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, mcs_state: bool) -> None:
		"""[SOURce<HW>]:BB:HUWB:FCONfig:MCS:STATe \n
		Activates MAC frame check sequence field. \n
			:param mcs_state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(mcs_state)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:FCONfig:MCS:STATe {param}')
