from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.RepeatedCapability import RepeatedCapability
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Channel:
	"""Channel commands group definition. 100 total commands, 14 Sub-groups, 1 group commands
	Repeated Capability: Channel, default value after init: Channel.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("channel", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_channel_get', 'repcap_channel_set', repcap.Channel.Nr1)

	def clone(self) -> 'Channel':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Channel(self._core, self._base.parent)
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
	def aich(self):
		"""aich commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_aich'):
			from .Channel_.Aich import Aich
			self._aich = Aich(self._core, self._base)
		return self._aich

	@property
	def apaich(self):
		"""apaich commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_apaich'):
			from .Channel_.Apaich import Apaich
			self._apaich = Apaich(self._core, self._base)
		return self._apaich

	@property
	def ccode(self):
		"""ccode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ccode'):
			from .Channel_.Ccode import Ccode
			self._ccode = Ccode(self._core, self._base)
		return self._ccode

	@property
	def data(self):
		"""data commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_data'):
			from .Channel_.Data import Data
			self._data = Data(self._core, self._base)
		return self._data

	@property
	def dpcch(self):
		"""dpcch commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_dpcch'):
			from .Channel_.Dpcch import Dpcch
			self._dpcch = Dpcch(self._core, self._base)
		return self._dpcch

	@property
	def fdpch(self):
		"""fdpch commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_fdpch'):
			from .Channel_.Fdpch import Fdpch
			self._fdpch = Fdpch(self._core, self._base)
		return self._fdpch

	@property
	def hsdpa(self):
		"""hsdpa commands group. 9 Sub-classes, 0 commands."""
		if not hasattr(self, '_hsdpa'):
			from .Channel_.Hsdpa import Hsdpa
			self._hsdpa = Hsdpa(self._core, self._base)
		return self._hsdpa

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .Channel_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power

	@property
	def sformat(self):
		"""sformat commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sformat'):
			from .Channel_.Sformat import Sformat
			self._sformat = Sformat(self._core, self._base)
		return self._sformat

	@property
	def symbolRate(self):
		"""symbolRate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_symbolRate'):
			from .Channel_.SymbolRate import SymbolRate
			self._symbolRate = SymbolRate(self._core, self._base)
		return self._symbolRate

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Channel_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def toffset(self):
		"""toffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_toffset'):
			from .Channel_.Toffset import Toffset
			self._toffset = Toffset(self._core, self._base)
		return self._toffset

	@property
	def typePy(self):
		"""typePy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_typePy'):
			from .Channel_.TypePy import TypePy
			self._typePy = TypePy(self._core, self._base)
		return self._typePy

	@property
	def hsupa(self):
		"""hsupa commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_hsupa'):
			from .Channel_.Hsupa import Hsupa
			self._hsupa = Hsupa(self._core, self._base)
		return self._hsupa

	def preset(self, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:BSTation<ST>:CHANnel:PRESet \n
		The command calls the default settings of the channel table. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:CHANnel:PRESet')

	def preset_with_opc(self, stream=repcap.Stream.Default) -> None:
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		"""[SOURce<HW>]:BB:W3GPp:BSTation<ST>:CHANnel:PRESet \n
		The command calls the default settings of the channel table. \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:CHANnel:PRESet')
