from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Info:
	"""Info commands group definition. 8 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("info", core, parent)

	def clone(self) -> 'Info':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Info(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def ecount(self):
		"""ecount commands group. 3 Sub-classes, 1 commands."""
		if not hasattr(self, '_ecount'):
			from .Info_.Ecount import Ecount
			self._ecount = Ecount(self._core, self._base)
		return self._ecount

	@property
	def otime(self):
		"""otime commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_otime'):
			from .Info_.Otime import Otime
			self._otime = Otime(self._core, self._base)
		return self._otime

	@property
	def poCount(self):
		"""poCount commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_poCount'):
			from .Info_.PoCount import PoCount
			self._poCount = PoCount(self._core, self._base)
		return self._poCount
