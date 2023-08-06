from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tpc:
	"""Tpc commands group definition. 4 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tpc", core, parent)

	def clone(self) -> 'Tpc':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Tpc(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def data(self):
		"""data commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_data'):
			from .Tpc_.Data import Data
			self._data = Data(self._core, self._base)
		return self._data

	@property
	def read(self):
		"""read commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_read'):
			from .Tpc_.Read import Read
			self._read = Read(self._core, self._base)
		return self._read
