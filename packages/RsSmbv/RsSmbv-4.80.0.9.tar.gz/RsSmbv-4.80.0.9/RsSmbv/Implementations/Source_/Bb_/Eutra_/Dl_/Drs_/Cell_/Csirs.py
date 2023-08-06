from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.RepeatedCapability import RepeatedCapability
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Csirs:
	"""Csirs commands group definition. 8 total commands, 8 Sub-groups, 0 group commands
	Repeated Capability: Stream, default value after init: Stream.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("csirs", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_stream_get', 'repcap_stream_set', repcap.Stream.Nr1)

	def clone(self) -> 'Csirs':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Csirs(self._core, self._base.parent)
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
	def nzConfig(self):
		"""nzConfig commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nzConfig'):
			from .Csirs_.NzConfig import NzConfig
			self._nzConfig = NzConfig(self._core, self._base)
		return self._nzConfig

	@property
	def nzqOffset(self):
		"""nzqOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nzqOffset'):
			from .Csirs_.NzqOffset import NzqOffset
			self._nzqOffset = NzqOffset(self._core, self._base)
		return self._nzqOffset

	@property
	def nzscid(self):
		"""nzscid commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nzscid'):
			from .Csirs_.Nzscid import Nzscid
			self._nzscid = Nzscid(self._core, self._base)
		return self._nzscid

	@property
	def nzsfOffset(self):
		"""nzsfOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nzsfOffset'):
			from .Csirs_.NzsfOffset import NzsfOffset
			self._nzsfOffset = NzsfOffset(self._core, self._base)
		return self._nzsfOffset

	@property
	def zp(self):
		"""zp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_zp'):
			from .Csirs_.Zp import Zp
			self._zp = Zp(self._core, self._base)
		return self._zp

	@property
	def zpDelta(self):
		"""zpDelta commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_zpDelta'):
			from .Csirs_.ZpDelta import ZpDelta
			self._zpDelta = ZpDelta(self._core, self._base)
		return self._zpDelta

	@property
	def zpi(self):
		"""zpi commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_zpi'):
			from .Csirs_.Zpi import Zpi
			self._zpi = Zpi(self._core, self._base)
		return self._zpi

	@property
	def zpt(self):
		"""zpt commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_zpt'):
			from .Csirs_.Zpt import Zpt
			self._zpt = Zpt(self._core, self._base)
		return self._zpt
