from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal.RepeatedCapability import RepeatedCapability
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Echo:
	"""Echo commands group definition. 7 total commands, 7 Sub-groups, 0 group commands
	Repeated Capability: Echoes, default value after init: Echoes.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("echo", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_echoes_get', 'repcap_echoes_set', repcap.Echoes.Nr1)

	def clone(self) -> 'Echo':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Echo(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	def repcap_echoes_set(self, enum_value: repcap.Echoes) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Echoes.Default
		Default value after init: Echoes.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_echoes_get(self) -> repcap.Echoes:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def aazimuth(self):
		"""aazimuth commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_aazimuth'):
			from .Echo_.Aazimuth import Aazimuth
			self._aazimuth = Aazimuth(self._core, self._base)
		return self._aazimuth

	@property
	def aelevation(self):
		"""aelevation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_aelevation'):
			from .Echo_.Aelevation import Aelevation
			self._aelevation = Aelevation(self._core, self._base)
		return self._aelevation

	@property
	def cpDrift(self):
		"""cpDrift commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cpDrift'):
			from .Echo_.CpDrift import CpDrift
			self._cpDrift = CpDrift(self._core, self._base)
		return self._cpDrift

	@property
	def cphase(self):
		"""cphase commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cphase'):
			from .Echo_.Cphase import Cphase
			self._cphase = Cphase(self._core, self._base)
		return self._cphase

	@property
	def dshift(self):
		"""dshift commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dshift'):
			from .Echo_.Dshift import Dshift
			self._dshift = Dshift(self._core, self._base)
		return self._dshift

	@property
	def icPhase(self):
		"""icPhase commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_icPhase'):
			from .Echo_.IcPhase import IcPhase
			self._icPhase = IcPhase(self._core, self._base)
		return self._icPhase

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .Echo_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power
