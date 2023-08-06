from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AsPy:
	"""AsPy commands group definition. 51 total commands, 5 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("asPy", core, parent)

	def clone(self) -> 'AsPy':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = AsPy(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def apply(self):
		"""apply commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_apply'):
			from .AsPy_.Apply import Apply
			self._apply = Apply(self._core, self._base)
		return self._apply

	@property
	def arbLen(self):
		"""arbLen commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_arbLen'):
			from .AsPy_.ArbLen import ArbLen
			self._arbLen = ArbLen(self._core, self._base)
		return self._arbLen

	@property
	def asLength(self):
		"""asLength commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_asLength'):
			from .AsPy_.AsLength import AsLength
			self._asLength = AsLength(self._core, self._base)
		return self._asLength

	@property
	def dl(self):
		"""dl commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_dl'):
			from .AsPy_.Dl import Dl
			self._dl = Dl(self._core, self._base)
		return self._dl

	@property
	def ul(self):
		"""ul commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_ul'):
			from .AsPy_.Ul import Ul
			self._ul = Ul(self._core, self._base)
		return self._ul
