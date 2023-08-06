from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Los:
	"""Los commands group definition. 8 total commands, 8 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("los", core, parent)

	def clone(self) -> 'Los':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Los(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def aazimuth(self):
		"""aazimuth commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_aazimuth'):
			from .Los_.Aazimuth import Aazimuth
			self._aazimuth = Aazimuth(self._core, self._base)
		return self._aazimuth

	@property
	def aelevation(self):
		"""aelevation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_aelevation'):
			from .Los_.Aelevation import Aelevation
			self._aelevation = Aelevation(self._core, self._base)
		return self._aelevation

	@property
	def cpDrift(self):
		"""cpDrift commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cpDrift'):
			from .Los_.CpDrift import CpDrift
			self._cpDrift = CpDrift(self._core, self._base)
		return self._cpDrift

	@property
	def cphase(self):
		"""cphase commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cphase'):
			from .Los_.Cphase import Cphase
			self._cphase = Cphase(self._core, self._base)
		return self._cphase

	@property
	def dshift(self):
		"""dshift commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dshift'):
			from .Los_.Dshift import Dshift
			self._dshift = Dshift(self._core, self._base)
		return self._dshift

	@property
	def enable(self):
		"""enable commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_enable'):
			from .Los_.Enable import Enable
			self._enable = Enable(self._core, self._base)
		return self._enable

	@property
	def icPhase(self):
		"""icPhase commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_icPhase'):
			from .Los_.IcPhase import IcPhase
			self._icPhase = IcPhase(self._core, self._base)
		return self._icPhase

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .Los_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power
