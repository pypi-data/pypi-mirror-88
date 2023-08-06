from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rt:
	"""Rt commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rt", core, parent)

	def get_changes(self) -> bool:
		"""[SOURce<HW>]:BB:GNSS:LOGGing:RT:CHANges \n
		No command help available \n
			:return: status: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:LOGGing:RT:CHANges?')
		return Conversions.str_to_bool(response)

	def set_changes(self, status: bool) -> None:
		"""[SOURce<HW>]:BB:GNSS:LOGGing:RT:CHANges \n
		No command help available \n
			:param status: No help available
		"""
		param = Conversions.bool_to_str(status)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:LOGGing:RT:CHANges {param}')

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:GNSS:LOGGing:RT:STATe \n
		Starts real-time data logging. \n
			:return: status: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:LOGGing:RT:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, status: bool) -> None:
		"""[SOURce<HW>]:BB:GNSS:LOGGing:RT:STATe \n
		Starts real-time data logging. \n
			:param status: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(status)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:LOGGing:RT:STATe {param}')
