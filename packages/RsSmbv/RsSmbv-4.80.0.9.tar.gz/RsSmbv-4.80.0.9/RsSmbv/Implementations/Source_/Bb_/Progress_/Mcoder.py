from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mcoder:
	"""Mcoder commands group definition. 5 total commands, 2 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mcoder", core, parent)

	def clone(self) -> 'Mcoder':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Mcoder(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def arbitrary(self):
		"""arbitrary commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_arbitrary'):
			from .Mcoder_.Arbitrary import Arbitrary
			self._arbitrary = Arbitrary(self._core, self._base)
		return self._arbitrary

	@property
	def dm(self):
		"""dm commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_dm'):
			from .Mcoder_.Dm import Dm
			self._dm = Dm(self._core, self._base)
		return self._dm

	def get_value(self) -> int:
		"""[SOURce<HW>]:BB:PROGress:MCODer \n
		Queries the status of an initiated process, like for example the calculation of a signal in accordance to a digital
		standard, or the calculation of a multi-carrier or multi-segment waveform file. \n
			:return: mcoder: integer Indicates the task progress in percent Range: 0 to 100
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:PROGress:MCODer?')
		return Conversions.str_to_int(response)
