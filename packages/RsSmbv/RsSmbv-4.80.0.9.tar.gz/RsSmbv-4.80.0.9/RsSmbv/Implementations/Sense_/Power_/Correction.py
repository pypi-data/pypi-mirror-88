from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Correction:
	"""Correction commands group definition. 3 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("correction", core, parent)

	def clone(self) -> 'Correction':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Correction(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def spDevice(self):
		"""spDevice commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_spDevice'):
			from .Correction_.SpDevice import SpDevice
			self._spDevice = SpDevice(self._core, self._base)
		return self._spDevice
