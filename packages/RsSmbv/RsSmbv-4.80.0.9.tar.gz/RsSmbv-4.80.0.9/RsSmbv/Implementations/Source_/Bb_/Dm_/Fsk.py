from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Fsk:
	"""Fsk commands group definition. 3 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("fsk", core, parent)

	def clone(self) -> 'Fsk':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Fsk(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def variable(self):
		"""variable commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_variable'):
			from .Fsk_.Variable import Variable
			self._variable = Variable(self._core, self._base)
		return self._variable

	def get_deviation(self) -> float:
		"""[SOURce<HW>]:BB:DM:FSK:DEViation \n
		Sets the frequency deviation when FSK modulation is selected. \n
			:return: deviation: float The value range depends on the symbol rate. Range: 1 to 40E6
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DM:FSK:DEViation?')
		return Conversions.str_to_float(response)

	def set_deviation(self, deviation: float) -> None:
		"""[SOURce<HW>]:BB:DM:FSK:DEViation \n
		Sets the frequency deviation when FSK modulation is selected. \n
			:param deviation: float The value range depends on the symbol rate. Range: 1 to 40E6
		"""
		param = Conversions.decimal_value_to_str(deviation)
		self._core.io.write(f'SOURce<HwInstance>:BB:DM:FSK:DEViation {param}')
