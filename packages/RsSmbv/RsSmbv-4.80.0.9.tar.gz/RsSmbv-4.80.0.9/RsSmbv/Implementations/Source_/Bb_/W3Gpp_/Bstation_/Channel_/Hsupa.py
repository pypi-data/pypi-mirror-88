from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Hsupa:
	"""Hsupa commands group definition. 18 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("hsupa", core, parent)

	def clone(self) -> 'Hsupa':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Hsupa(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def eagch(self):
		"""eagch commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_eagch'):
			from .Hsupa_.Eagch import Eagch
			self._eagch = Eagch(self._core, self._base)
		return self._eagch

	@property
	def ehich(self):
		"""ehich commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_ehich'):
			from .Hsupa_.Ehich import Ehich
			self._ehich = Ehich(self._core, self._base)
		return self._ehich

	@property
	def ergch(self):
		"""ergch commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_ergch'):
			from .Hsupa_.Ergch import Ergch
			self._ergch = Ergch(self._core, self._base)
		return self._ergch
