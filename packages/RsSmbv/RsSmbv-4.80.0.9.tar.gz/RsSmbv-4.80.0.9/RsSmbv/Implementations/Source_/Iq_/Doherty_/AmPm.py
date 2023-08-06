from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AmPm:
	"""AmPm commands group definition. 3 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("amPm", core, parent)

	def clone(self) -> 'AmPm':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = AmPm(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def value(self):
		"""value commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_value'):
			from .AmPm_.Value import Value
			self._value = Value(self._core, self._base)
		return self._value
