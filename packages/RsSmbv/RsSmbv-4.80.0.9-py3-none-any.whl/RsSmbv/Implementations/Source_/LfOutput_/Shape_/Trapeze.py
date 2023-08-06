from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Trapeze:
	"""Trapeze commands group definition. 4 total commands, 4 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("trapeze", core, parent)

	def clone(self) -> 'Trapeze':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Trapeze(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def fall(self):
		"""fall commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fall'):
			from .Trapeze_.Fall import Fall
			self._fall = Fall(self._core, self._base)
		return self._fall

	@property
	def high(self):
		"""high commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_high'):
			from .Trapeze_.High import High
			self._high = High(self._core, self._base)
		return self._high

	@property
	def period(self):
		"""period commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_period'):
			from .Trapeze_.Period import Period
			self._period = Period(self._core, self._base)
		return self._period

	@property
	def rise(self):
		"""rise commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rise'):
			from .Trapeze_.Rise import Rise
			self._rise = Rise(self._core, self._base)
		return self._rise
