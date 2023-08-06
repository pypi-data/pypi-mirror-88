from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Output:
	"""Output commands group definition. 88 total commands, 2 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("output", core, parent)

	def clone(self) -> 'Output':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Output(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def analog(self):
		"""analog commands group. 6 Sub-classes, 4 commands."""
		if not hasattr(self, '_analog'):
			from .Output_.Analog import Analog
			self._analog = Analog(self._core, self._base)
		return self._analog

	@property
	def digital(self):
		"""digital commands group. 6 Sub-classes, 4 commands."""
		if not hasattr(self, '_digital'):
			from .Output_.Digital import Digital
			self._digital = Digital(self._core, self._base)
		return self._digital

	def get_level(self) -> float:
		"""[SOURce<HW>]:IQ:OUTPut:LEVel \n
		Sets the off-load voltage Vp of the analog I/Q signal output. The value range is adjusted so that the maximum overall
		output voltage does not exceed 4V, see 'Maximum overall output voltage'. \n
			:return: level: float Range: 0.02V to 4V , Unit: V
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:LEVel?')
		return Conversions.str_to_float(response)

	def set_level(self, level: float) -> None:
		"""[SOURce<HW>]:IQ:OUTPut:LEVel \n
		Sets the off-load voltage Vp of the analog I/Q signal output. The value range is adjusted so that the maximum overall
		output voltage does not exceed 4V, see 'Maximum overall output voltage'. \n
			:param level: float Range: 0.02V to 4V , Unit: V
		"""
		param = Conversions.decimal_value_to_str(level)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:LEVel {param}')
