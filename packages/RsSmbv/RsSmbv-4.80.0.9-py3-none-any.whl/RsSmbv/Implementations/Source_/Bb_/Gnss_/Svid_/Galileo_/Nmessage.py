from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Nmessage:
	"""Nmessage commands group definition. 93 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("nmessage", core, parent)

	def clone(self) -> 'Nmessage':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Nmessage(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def fnav(self):
		"""fnav commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_fnav'):
			from .Nmessage_.Fnav import Fnav
			self._fnav = Fnav(self._core, self._base)
		return self._fnav

	@property
	def inav(self):
		"""inav commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_inav'):
			from .Nmessage_.Inav import Inav
			self._inav = Inav(self._core, self._base)
		return self._inav
