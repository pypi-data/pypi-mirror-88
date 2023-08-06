from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Hpps:
	"""Hpps commands group definition. 2 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("hpps", core, parent)

	def clone(self) -> 'Hpps':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Hpps(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def adelay(self):
		"""adelay commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_adelay'):
			from .Hpps_.Adelay import Adelay
			self._adelay = Adelay(self._core, self._base)
		return self._adelay

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Hpps_.State import State
			self._state = State(self._core, self._base)
		return self._state
