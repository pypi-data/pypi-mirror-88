from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Fs:
	"""Fs commands group definition. 4 total commands, 4 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("fs", core, parent)

	def clone(self) -> 'Fs':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Fs(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def cycShift(self):
		"""cycShift commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cycShift'):
			from .Fs_.CycShift import CycShift
			self._cycShift = CycShift(self._core, self._base)
		return self._cycShift

	@property
	def occLength(self):
		"""occLength commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_occLength'):
			from .Fs_.OccLength import OccLength
			self._occLength = OccLength(self._core, self._base)
		return self._occLength

	@property
	def occIndex(self):
		"""occIndex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_occIndex'):
			from .Fs_.OccIndex import OccIndex
			self._occIndex = OccIndex(self._core, self._base)
		return self._occIndex

	@property
	def tdocc(self):
		"""tdocc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tdocc'):
			from .Fs_.Tdocc import Tdocc
			self._tdocc = Tdocc(self._core, self._base)
		return self._tdocc
