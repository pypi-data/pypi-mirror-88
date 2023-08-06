from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Option:
	"""Option commands group definition. 2 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("option", core, parent)

	def clone(self) -> 'Option':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Option(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def trial(self):
		"""trial commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_trial'):
			from .Option_.Trial import Trial
			self._trial = Trial(self._core, self._base)
		return self._trial
