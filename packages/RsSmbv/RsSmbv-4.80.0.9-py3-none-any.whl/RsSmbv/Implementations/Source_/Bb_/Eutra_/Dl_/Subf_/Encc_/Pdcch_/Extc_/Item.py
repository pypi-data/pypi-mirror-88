from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal.RepeatedCapability import RepeatedCapability
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Item:
	"""Item commands group definition. 57 total commands, 12 Sub-groups, 0 group commands
	Repeated Capability: Channel, default value after init: Channel.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("item", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_channel_get', 'repcap_channel_set', repcap.Channel.Nr1)

	def clone(self) -> 'Item':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Item(self._core, self._base.parent)
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
		"""cell commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cell'):
			from .Item_.Cell import Cell
			self._cell = Cell(self._core, self._base)
		return self._cell

	@property
	def cindex(self):
		"""cindex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cindex'):
			from .Item_.Cindex import Cindex
			self._cindex = Cindex(self._core, self._base)
		return self._cindex

	@property
	def conflict(self):
		"""conflict commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_conflict'):
			from .Item_.Conflict import Conflict
			self._conflict = Conflict(self._core, self._base)
		return self._conflict

	@property
	def dciConf(self):
		"""dciConf commands group. 37 Sub-classes, 0 commands."""
		if not hasattr(self, '_dciConf'):
			from .Item_.DciConf import DciConf
			self._dciConf = DciConf(self._core, self._base)
		return self._dciConf

	@property
	def dciFmt(self):
		"""dciFmt commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dciFmt'):
			from .Item_.DciFmt import DciFmt
			self._dciFmt = DciFmt(self._core, self._base)
		return self._dciFmt

	@property
	def ncces(self):
		"""ncces commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ncces'):
			from .Item_.Ncces import Ncces
			self._ncces = Ncces(self._core, self._base)
		return self._ncces

	@property
	def ndcces(self):
		"""ndcces commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ndcces'):
			from .Item_.Ndcces import Ndcces
			self._ndcces = Ndcces(self._core, self._base)
		return self._ndcces

	@property
	def pdcchType(self):
		"""pdcchType commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pdcchType'):
			from .Item_.PdcchType import PdcchType
			self._pdcchType = PdcchType(self._core, self._base)
		return self._pdcchType

	@property
	def pfmt(self):
		"""pfmt commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pfmt'):
			from .Item_.Pfmt import Pfmt
			self._pfmt = Pfmt(self._core, self._base)
		return self._pfmt

	@property
	def sespace(self):
		"""sespace commands group. 3 Sub-classes, 1 commands."""
		if not hasattr(self, '_sespace'):
			from .Item_.Sespace import Sespace
			self._sespace = Sespace(self._core, self._base)
		return self._sespace

	@property
	def ueid(self):
		"""ueid commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ueid'):
			from .Item_.Ueid import Ueid
			self._ueid = Ueid(self._core, self._base)
		return self._ueid

	@property
	def user(self):
		"""user commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_user'):
			from .Item_.User import User
			self._user = User(self._core, self._base)
		return self._user
