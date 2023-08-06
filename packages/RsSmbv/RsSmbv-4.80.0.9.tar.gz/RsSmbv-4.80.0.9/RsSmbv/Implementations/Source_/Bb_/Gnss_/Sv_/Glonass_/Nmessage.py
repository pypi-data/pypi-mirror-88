from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Nmessage:
	"""Nmessage commands group definition. 9 total commands, 1 Sub-groups, 0 group commands"""

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
	def nav(self):
		"""nav commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_nav'):
			from .Nmessage_.Nav import Nav
			self._nav = Nav(self._core, self._base)
		return self._nav
