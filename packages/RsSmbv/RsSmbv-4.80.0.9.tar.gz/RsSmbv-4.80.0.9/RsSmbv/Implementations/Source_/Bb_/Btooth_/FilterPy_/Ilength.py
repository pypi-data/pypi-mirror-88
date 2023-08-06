from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ilength:
	"""Ilength commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ilength", core, parent)

	def clone(self) -> 'Ilength':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Ilength(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def auto(self):
		"""auto commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_auto'):
			from .Ilength_.Auto import Auto
			self._auto = Auto(self._core, self._base)
		return self._auto

	def get_value(self) -> int:
		"""[SOURce<HW>]:BB:BTOoth:FILTer:ILENgth \n
		Sets the impulse length (the number of filter taps) . \n
			:return: ilrngth: integer Range: 1 to depends on oversampling
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:FILTer:ILENgth?')
		return Conversions.str_to_int(response)

	def set_value(self, ilrngth: int) -> None:
		"""[SOURce<HW>]:BB:BTOoth:FILTer:ILENgth \n
		Sets the impulse length (the number of filter taps) . \n
			:param ilrngth: integer Range: 1 to depends on oversampling
		"""
		param = Conversions.decimal_value_to_str(ilrngth)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:FILTer:ILENgth {param}')
