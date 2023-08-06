from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class HilPosition:
	"""HilPosition commands group definition. 2 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("hilPosition", core, parent)

	def clone(self) -> 'HilPosition':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = HilPosition(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def latency(self):
		"""latency commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_latency'):
			from .HilPosition_.Latency import Latency
			self._latency = Latency(self._core, self._base)
		return self._latency
