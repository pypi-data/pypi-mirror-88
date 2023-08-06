from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.RepeatedCapability import RepeatedCapability
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class User:
	"""User commands group definition. 270 total commands, 7 Sub-groups, 0 group commands
	Repeated Capability: Channel, default value after init: Channel.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("user", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_channel_get', 'repcap_channel_set', repcap.Channel.Nr1)

	def clone(self) -> 'User':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = User(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	def repcap_channel_set(self, enum_value: repcap.Channel) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Channel.Default
		Default value after init: Channel.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_channel_get(self) -> repcap.Channel:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def cell(self):
		"""cell commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_cell'):
			from .User_.Cell import Cell
			self._cell = Cell(self._core, self._base)
		return self._cell

	@property
	def dsch(self):
		"""dsch commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_dsch'):
			from .User_.Dsch import Dsch
			self._dsch = Dsch(self._core, self._base)
		return self._dsch

	@property
	def ncarrier(self):
		"""ncarrier commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ncarrier'):
			from .User_.Ncarrier import Ncarrier
			self._ncarrier = Ncarrier(self._core, self._base)
		return self._ncarrier

	@property
	def numSfi(self):
		"""numSfi commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_numSfi'):
			from .User_.NumSfi import NumSfi
			self._numSfi = NumSfi(self._core, self._base)
		return self._numSfi

	@property
	def rnti(self):
		"""rnti commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_rnti'):
			from .User_.Rnti import Rnti
			self._rnti = Rnti(self._core, self._base)
		return self._rnti

	@property
	def ueid(self):
		"""ueid commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ueid'):
			from .User_.Ueid import Ueid
			self._ueid = Ueid(self._core, self._base)
		return self._ueid

	@property
	def usch(self):
		"""usch commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_usch'):
			from .User_.Usch import Usch
			self._usch = Usch(self._core, self._base)
		return self._usch
