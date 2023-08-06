from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class All:
	"""All commands group definition. 5 total commands, 1 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("all", core, parent)

	def clone(self) -> 'All':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = All(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def measure(self):
		"""measure commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_measure'):
			from .All_.Measure import Measure
			self._measure = Measure(self._core, self._base)
		return self._measure

	def get_date(self) -> str:
		"""CALibration<HW>:ALL:DATE \n
		Queries the date of the most recently executed full adjustment. \n
			:return: date: string
		"""
		response = self._core.io.query_str('CALibration<HwInstance>:ALL:DATE?')
		return trim_str_response(response)

	def get_information(self) -> str:
		"""CALibration<HW>:ALL:INFormation \n
		Queries the current state of the internal adjustment. \n
			:return: cal_info_text: string
		"""
		response = self._core.io.query_str('CALibration<HwInstance>:ALL:INFormation?')
		return trim_str_response(response)

	def get_temp(self) -> str:
		"""CALibration<HW>:ALL:TEMP \n
		Queries the temperature deviation compared to the calibration temperature. \n
			:return: temperature: string
		"""
		response = self._core.io.query_str('CALibration<HwInstance>:ALL:TEMP?')
		return trim_str_response(response)

	def get_time(self) -> str:
		"""CALibration<HW>:ALL:TIME \n
		Queries the time elapsed since the last full adjustment. \n
			:return: time: string
		"""
		response = self._core.io.query_str('CALibration<HwInstance>:ALL:TIME?')
		return trim_str_response(response)
