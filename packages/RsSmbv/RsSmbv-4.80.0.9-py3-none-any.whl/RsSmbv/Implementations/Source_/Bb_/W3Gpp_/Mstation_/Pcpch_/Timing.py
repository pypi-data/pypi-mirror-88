from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Timing:
	"""Timing commands group definition. 6 total commands, 4 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("timing", core, parent)

	def clone(self) -> 'Timing':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Timing(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def dpower(self):
		"""dpower commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_dpower'):
			from .Timing_.Dpower import Dpower
			self._dpower = Dpower(self._core, self._base)
		return self._dpower

	@property
	def soffset(self):
		"""soffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_soffset'):
			from .Timing_.Soffset import Soffset
			self._soffset = Soffset(self._core, self._base)
		return self._soffset

	@property
	def speriod(self):
		"""speriod commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_speriod'):
			from .Timing_.Speriod import Speriod
			self._speriod = Speriod(self._core, self._base)
		return self._speriod

	@property
	def time(self):
		"""time commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_time'):
			from .Timing_.Time import Time
			self._time = Time(self._core, self._base)
		return self._time
