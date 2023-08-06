from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Srs:
	"""Srs commands group definition. 28 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("srs", core, parent)

	def clone(self) -> 'Srs':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Srs(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def naPort(self):
		"""naPort commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_naPort'):
			from .Srs_.NaPort import NaPort
			self._naPort = NaPort(self._core, self._base)
		return self._naPort

	@property
	def rs(self):
		"""rs commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_rs'):
			from .Srs_.Rs import Rs
			self._rs = Rs(self._core, self._base)
		return self._rs

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Srs_.State import State
			self._state = State(self._core, self._base)
		return self._state
