from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Frequency:
	"""Frequency commands group definition. 4 total commands, 4 Sub-groups, 0 group commands"""

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

	@property
	def cw(self):
		"""cw commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cw'):
			from .Frequency_.Cw import Cw
			self._cw = Cw(self._core, self._base)
		return self._cw

	@property
	def reference(self):
		"""reference commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_reference'):
			from .Frequency_.Reference import Reference
			self._reference = Reference(self._core, self._base)
		return self._reference

	@property
	def target(self):
		"""target commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_target'):
			from .Frequency_.Target import Target
			self._target = Target(self._core, self._base)
		return self._target
