from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.RepeatedCapability import RepeatedCapability
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Set:
	"""Set commands group definition. 10 total commands, 10 Sub-groups, 0 group commands
	Repeated Capability: Direction, default value after init: Direction.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("set", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_direction_get', 'repcap_direction_set', repcap.Direction.Nr1)

	def clone(self) -> 'Set':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Set(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	def repcap_direction_set(self, enum_value: repcap.Direction) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Direction.Default
		Default value after init: Direction.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_direction_get(self) -> repcap.Direction:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def hopping(self):
		"""hopping commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hopping'):
			from .Set_.Hopping import Hopping
			self._hopping = Hopping(self._core, self._base)
		return self._hopping

	@property
	def nid(self):
		"""nid commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nid'):
			from .Set_.Nid import Nid
			self._nid = Nid(self._core, self._base)
		return self._nid

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .Set_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power

	@property
	def prbs(self):
		"""prbs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_prbs'):
			from .Set_.Prbs import Prbs
			self._prbs = Prbs(self._core, self._base)
		return self._prbs

	@property
	def rba(self):
		"""rba commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rba'):
			from .Set_.Rba import Rba
			self._rba = Rba(self._core, self._base)
		return self._rba

	@property
	def repmpdcch(self):
		"""repmpdcch commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_repmpdcch'):
			from .Set_.Repmpdcch import Repmpdcch
			self._repmpdcch = Repmpdcch(self._core, self._base)
		return self._repmpdcch

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Set_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def stnb(self):
		"""stnb commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_stnb'):
			from .Set_.Stnb import Stnb
			self._stnb = Stnb(self._core, self._base)
		return self._stnb

	@property
	def stsf(self):
		"""stsf commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_stsf'):
			from .Set_.Stsf import Stsf
			self._stsf = Stsf(self._core, self._base)
		return self._stsf

	@property
	def ttyp(self):
		"""ttyp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ttyp'):
			from .Set_.Ttyp import Ttyp
			self._ttyp = Ttyp(self._core, self._base)
		return self._ttyp
