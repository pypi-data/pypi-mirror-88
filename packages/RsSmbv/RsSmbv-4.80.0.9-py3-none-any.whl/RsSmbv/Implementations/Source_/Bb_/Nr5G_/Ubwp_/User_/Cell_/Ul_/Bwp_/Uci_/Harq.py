from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Harq:
	"""Harq commands group definition. 3 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("harq", core, parent)

	def clone(self) -> 'Harq':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Harq(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def off0(self):
		"""off0 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_off0'):
			from .Harq_.Off0 import Off0
			self._off0 = Off0(self._core, self._base)
		return self._off0

	@property
	def off1(self):
		"""off1 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_off1'):
			from .Harq_.Off1 import Off1
			self._off1 = Off1(self._core, self._base)
		return self._off1

	@property
	def off2(self):
		"""off2 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_off2'):
			from .Harq_.Off2 import Off2
			self._off2 = Off2(self._core, self._base)
		return self._off2
