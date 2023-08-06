from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.RepeatedCapability import RepeatedCapability
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Cell:
	"""Cell commands group definition. 142 total commands, 12 Sub-groups, 0 group commands
	Repeated Capability: Stream, default value after init: Stream.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cell", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_stream_get', 'repcap_stream_set', repcap.Stream.Nr1)

	def clone(self) -> 'Cell':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Cell(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	def repcap_stream_set(self, enum_value: repcap.Stream) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Stream.Default
		Default value after init: Stream.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_stream_get(self) -> repcap.Stream:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def dwpts(self):
		"""dwpts commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_dwpts'):
			from .Cell_.Dwpts import Dwpts
			self._dwpts = Dwpts(self._core, self._base)
		return self._dwpts

	@property
	def enh(self):
		"""enh commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_enh'):
			from .Cell_.Enh import Enh
			self._enh = Enh(self._core, self._base)
		return self._enh

	@property
	def mcode(self):
		"""mcode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mcode'):
			from .Cell_.Mcode import Mcode
			self._mcode = Mcode(self._core, self._base)
		return self._mcode

	@property
	def protation(self):
		"""protation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_protation'):
			from .Cell_.Protation import Protation
			self._protation = Protation(self._core, self._base)
		return self._protation

	@property
	def scode(self):
		"""scode commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_scode'):
			from .Cell_.Scode import Scode
			self._scode = Scode(self._core, self._base)
		return self._scode

	@property
	def sdCode(self):
		"""sdCode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sdCode'):
			from .Cell_.SdCode import SdCode
			self._sdCode = SdCode(self._core, self._base)
		return self._sdCode

	@property
	def slot(self):
		"""slot commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_slot'):
			from .Cell_.Slot import Slot
			self._slot = Slot(self._core, self._base)
		return self._slot

	@property
	def spoint(self):
		"""spoint commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_spoint'):
			from .Cell_.Spoint import Spoint
			self._spoint = Spoint(self._core, self._base)
		return self._spoint

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Cell_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def suCode(self):
		"""suCode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_suCode'):
			from .Cell_.SuCode import SuCode
			self._suCode = SuCode(self._core, self._base)
		return self._suCode

	@property
	def tdelay(self):
		"""tdelay commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tdelay'):
			from .Cell_.Tdelay import Tdelay
			self._tdelay = Tdelay(self._core, self._base)
		return self._tdelay

	@property
	def users(self):
		"""users commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_users'):
			from .Cell_.Users import Users
			self._users = Users(self._core, self._base)
		return self._users
