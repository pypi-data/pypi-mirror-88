from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Frequency:
	"""Frequency commands group definition. 3 total commands, 1 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("frequency", core, parent)

	def clone(self) -> 'Frequency':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Frequency(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def center(self):
		"""center commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_center'):
			from .Frequency_.Center import Center
			self._center = Center(self._core, self._base)
		return self._center

	def get_result(self) -> float:
		"""[SOURce<HW>]:AWGN:FREQuency:RESult \n
		Queries the actual frequency of the sine wave. \n
			:return: result: float Range: -40E6 to 40E6
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AWGN:FREQuency:RESult?')
		return Conversions.str_to_float(response)

	def get_target(self) -> float:
		"""[SOURce<HW>]:AWGN:FREQuency:TARGet \n
		Sets the desired frequency of the sine wave. \n
			:return: target: float Range: -40E6 to 40E6
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:AWGN:FREQuency:TARGet?')
		return Conversions.str_to_float(response)

	def set_target(self, target: float) -> None:
		"""[SOURce<HW>]:AWGN:FREQuency:TARGet \n
		Sets the desired frequency of the sine wave. \n
			:param target: float Range: -40E6 to 40E6
		"""
		param = Conversions.decimal_value_to_str(target)
		self._core.io.write(f'SOURce<HwInstance>:AWGN:FREQuency:TARGet {param}')
