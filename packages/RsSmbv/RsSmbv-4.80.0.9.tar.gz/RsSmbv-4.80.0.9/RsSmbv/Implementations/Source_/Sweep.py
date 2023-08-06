from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sweep:
	"""Sweep commands group definition. 29 total commands, 3 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sweep", core, parent)

	def clone(self) -> 'Sweep':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Sweep(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def combined(self):
		"""combined commands group. 1 Sub-classes, 5 commands."""
		if not hasattr(self, '_combined'):
			from .Sweep_.Combined import Combined
			self._combined = Combined(self._core, self._base)
		return self._combined

	@property
	def power(self):
		"""power commands group. 5 Sub-classes, 5 commands."""
		if not hasattr(self, '_power'):
			from .Sweep_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power

	@property
	def frequency(self):
		"""frequency commands group. 3 Sub-classes, 6 commands."""
		if not hasattr(self, '_frequency'):
			from .Sweep_.Frequency import Frequency
			self._frequency = Frequency(self._core, self._base)
		return self._frequency

	def reset_all(self) -> None:
		"""[SOURce<HW>]:SWEep:RESet:[ALL] \n
		Resets all active sweeps to the starting point. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:SWEep:RESet:ALL')

	def reset_all_with_opc(self) -> None:
		"""[SOURce<HW>]:SWEep:RESet:[ALL] \n
		Resets all active sweeps to the starting point. \n
		Same as reset_all, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:SWEep:RESet:ALL')
