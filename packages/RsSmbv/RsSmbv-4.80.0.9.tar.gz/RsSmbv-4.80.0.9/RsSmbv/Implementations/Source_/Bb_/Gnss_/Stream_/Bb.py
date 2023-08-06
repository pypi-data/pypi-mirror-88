from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Bb:
	"""Bb commands group definition. 4 total commands, 4 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("bb", core, parent)

	def clone(self) -> 'Bb':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Bb(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def channels(self):
		"""channels commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_channels'):
			from .Bb_.Channels import Channels
			self._channels = Channels(self._core, self._base)
		return self._channels

	@property
	def count(self):
		"""count commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_count'):
			from .Bb_.Count import Count
			self._count = Count(self._core, self._base)
		return self._count

	@property
	def info(self):
		"""info commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_info'):
			from .Bb_.Info import Info
			self._info = Info(self._core, self._base)
		return self._info

	@property
	def listPy(self):
		"""listPy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_listPy'):
			from .Bb_.ListPy import ListPy
			self._listPy = ListPy(self._core, self._base)
		return self._listPy
