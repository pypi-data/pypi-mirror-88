from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sc:
	"""Sc commands group definition. 2 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sc", core, parent)

	def clone(self) -> 'Sc':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Sc(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def active(self):
		"""active commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_active'):
			from .Sc_.Active import Active
			self._active = Active(self._core, self._base)
		return self._active

	@property
	def enabled(self):
		"""enabled commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_enabled'):
			from .Sc_.Enabled import Enabled
			self._enabled = Enabled(self._core, self._base)
		return self._enabled
