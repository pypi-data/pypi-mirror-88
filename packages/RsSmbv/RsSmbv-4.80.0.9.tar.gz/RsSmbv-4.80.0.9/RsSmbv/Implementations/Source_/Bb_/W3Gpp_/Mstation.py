from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.RepeatedCapability import RepeatedCapability
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mstation:
	"""Mstation commands group definition. 260 total commands, 14 Sub-groups, 1 group commands
	Repeated Capability: Stream, default value after init: Stream.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mstation", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_stream_get', 'repcap_stream_set', repcap.Stream.Nr1)

	def clone(self) -> 'Mstation':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Mstation(self._core, self._base.parent)
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
	def additional(self):
		"""additional commands group. 3 Sub-classes, 2 commands."""
		if not hasattr(self, '_additional'):
			from .Mstation_.Additional import Additional
			self._additional = Additional(self._core, self._base)
		return self._additional

	@property
	def channel(self):
		"""channel commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_channel'):
			from .Mstation_.Channel import Channel
			self._channel = Channel(self._core, self._base)
		return self._channel

	@property
	def cmode(self):
		"""cmode commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_cmode'):
			from .Mstation_.Cmode import Cmode
			self._cmode = Cmode(self._core, self._base)
		return self._cmode

	@property
	def dpcch(self):
		"""dpcch commands group. 8 Sub-classes, 0 commands."""
		if not hasattr(self, '_dpcch'):
			from .Mstation_.Dpcch import Dpcch
			self._dpcch = Dpcch(self._core, self._base)
		return self._dpcch

	@property
	def dpdch(self):
		"""dpdch commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_dpdch'):
			from .Mstation_.Dpdch import Dpdch
			self._dpdch = Dpdch(self._core, self._base)
		return self._dpdch

	@property
	def enhanced(self):
		"""enhanced commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_enhanced'):
			from .Mstation_.Enhanced import Enhanced
			self._enhanced = Enhanced(self._core, self._base)
		return self._enhanced

	@property
	def mode(self):
		"""mode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mode'):
			from .Mstation_.Mode import Mode
			self._mode = Mode(self._core, self._base)
		return self._mode

	@property
	def pcpch(self):
		"""pcpch commands group. 18 Sub-classes, 0 commands."""
		if not hasattr(self, '_pcpch'):
			from .Mstation_.Pcpch import Pcpch
			self._pcpch = Pcpch(self._core, self._base)
		return self._pcpch

	@property
	def prach(self):
		"""prach commands group. 15 Sub-classes, 0 commands."""
		if not hasattr(self, '_prach'):
			from .Mstation_.Prach import Prach
			self._prach = Prach(self._core, self._base)
		return self._prach

	@property
	def scode(self):
		"""scode commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_scode'):
			from .Mstation_.Scode import Scode
			self._scode = Scode(self._core, self._base)
		return self._scode

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Mstation_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def tdelay(self):
		"""tdelay commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tdelay'):
			from .Mstation_.Tdelay import Tdelay
			self._tdelay = Tdelay(self._core, self._base)
		return self._tdelay

	@property
	def udtx(self):
		"""udtx commands group. 6 Sub-classes, 6 commands."""
		if not hasattr(self, '_udtx'):
			from .Mstation_.Udtx import Udtx
			self._udtx = Udtx(self._core, self._base)
		return self._udtx

	@property
	def hsupa(self):
		"""hsupa commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_hsupa'):
			from .Mstation_.Hsupa import Hsupa
			self._hsupa = Hsupa(self._core, self._base)
		return self._hsupa

	def preset(self) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation:PRESet \n
		The command produces a standardized default for all the user equipment. The settings correspond to the *RST values
		specified for the commands. All user equipment settings are preset. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation:PRESet')

	def preset_with_opc(self) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation:PRESet \n
		The command produces a standardized default for all the user equipment. The settings correspond to the *RST values
		specified for the commands. All user equipment settings are preset. \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:W3GPp:MSTation:PRESet')
