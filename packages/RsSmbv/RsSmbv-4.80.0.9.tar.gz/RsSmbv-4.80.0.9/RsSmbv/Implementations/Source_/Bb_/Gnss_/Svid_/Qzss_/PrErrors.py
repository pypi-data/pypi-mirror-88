from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PrErrors:
	"""PrErrors commands group definition. 11 total commands, 4 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("prErrors", core, parent)

	def clone(self) -> 'PrErrors':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PrErrors(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def copy(self):
		"""copy commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_copy'):
			from .PrErrors_.Copy import Copy
			self._copy = Copy(self._core, self._base)
		return self._copy

	@property
	def mode(self):
		"""mode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mode'):
			from .PrErrors_.Mode import Mode
			self._mode = Mode(self._core, self._base)
		return self._mode

	@property
	def profile(self):
		"""profile commands group. 6 Sub-classes, 1 commands."""
		if not hasattr(self, '_profile'):
			from .PrErrors_.Profile import Profile
			self._profile = Profile(self._core, self._base)
		return self._profile

	@property
	def value(self):
		"""value commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_value'):
			from .PrErrors_.Value import Value
			self._value = Value(self._core, self._base)
		return self._value
