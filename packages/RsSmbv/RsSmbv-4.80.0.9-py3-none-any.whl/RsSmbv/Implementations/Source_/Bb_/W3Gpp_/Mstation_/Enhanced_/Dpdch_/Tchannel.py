from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.RepeatedCapability import RepeatedCapability
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tchannel:
	"""Tchannel commands group definition. 11 total commands, 9 Sub-groups, 0 group commands
	Repeated Capability: TransportChannel, default value after init: TransportChannel.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tchannel", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_transportChannel_get', 'repcap_transportChannel_set', repcap.TransportChannel.Nr0)

	def clone(self) -> 'Tchannel':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Tchannel(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	def repcap_transportChannel_set(self, enum_value: repcap.TransportChannel) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to TransportChannel.Default
		Default value after init: TransportChannel.Nr0"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_transportChannel_get(self) -> repcap.TransportChannel:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def crcSize(self):
		"""crcSize commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_crcSize'):
			from .Tchannel_.CrcSize import CrcSize
			self._crcSize = CrcSize(self._core, self._base)
		return self._crcSize

	@property
	def data(self):
		"""data commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_data'):
			from .Tchannel_.Data import Data
			self._data = Data(self._core, self._base)
		return self._data

	@property
	def eprotection(self):
		"""eprotection commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_eprotection'):
			from .Tchannel_.Eprotection import Eprotection
			self._eprotection = Eprotection(self._core, self._base)
		return self._eprotection

	@property
	def interleaver(self):
		"""interleaver commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_interleaver'):
			from .Tchannel_.Interleaver import Interleaver
			self._interleaver = Interleaver(self._core, self._base)
		return self._interleaver

	@property
	def rmAttribute(self):
		"""rmAttribute commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rmAttribute'):
			from .Tchannel_.RmAttribute import RmAttribute
			self._rmAttribute = RmAttribute(self._core, self._base)
		return self._rmAttribute

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Tchannel_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def tbCount(self):
		"""tbCount commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tbCount'):
			from .Tchannel_.TbCount import TbCount
			self._tbCount = TbCount(self._core, self._base)
		return self._tbCount

	@property
	def tbSize(self):
		"""tbSize commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tbSize'):
			from .Tchannel_.TbSize import TbSize
			self._tbSize = TbSize(self._core, self._base)
		return self._tbSize

	@property
	def ttInterval(self):
		"""ttInterval commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ttInterval'):
			from .Tchannel_.TtInterval import TtInterval
			self._ttInterval = TtInterval(self._core, self._base)
		return self._ttInterval
