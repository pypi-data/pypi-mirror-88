from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sweep:
	"""Sweep commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sweep", core, parent)

	def get_time(self) -> float:
		"""[SOURce<HW>]:BB:PRAMp:RAMP:SWEep:TIME \n
		No command help available \n
			:return: sweep_time: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:PRAMp:RAMP:SWEep:TIME?')
		return Conversions.str_to_float(response)

	def set_time(self, sweep_time: float) -> None:
		"""[SOURce<HW>]:BB:PRAMp:RAMP:SWEep:TIME \n
		No command help available \n
			:param sweep_time: No help available
		"""
		param = Conversions.decimal_value_to_str(sweep_time)
		self._core.io.write(f'SOURce<HwInstance>:BB:PRAMp:RAMP:SWEep:TIME {param}')
