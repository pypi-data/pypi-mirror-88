from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.RepeatedCapability import RepeatedCapability
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mstation:
	"""Mstation commands group definition. 27 total commands, 8 Sub-groups, 1 group commands
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
	def ccoding(self):
		"""ccoding commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ccoding'):
			from .Mstation_.Ccoding import Ccoding
			self._ccoding = Ccoding(self._core, self._base)
		return self._ccoding

	@property
	def channel(self):
		"""channel commands group. 7 Sub-classes, 0 commands."""
		if not hasattr(self, '_channel'):
			from .Mstation_.Channel import Channel
			self._channel = Channel(self._core, self._base)
		return self._channel

	@property
	def lcMask(self):
		"""lcMask commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_lcMask'):
			from .Mstation_.LcMask import LcMask
			self._lcMask = LcMask(self._core, self._base)
		return self._lcMask

	@property
	def mode(self):
		"""mode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mode'):
			from .Mstation_.Mode import Mode
			self._mode = Mode(self._core, self._base)
		return self._mode

	@property
	def rconfiguration(self):
		"""rconfiguration commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rconfiguration'):
			from .Mstation_.Rconfiguration import Rconfiguration
			self._rconfiguration = Rconfiguration(self._core, self._base)
		return self._rconfiguration

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Mstation_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def tpc(self):
		"""tpc commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_tpc'):
			from .Mstation_.Tpc import Tpc
			self._tpc = Tpc(self._core, self._base)
		return self._tpc

	def preset(self) -> None:
		"""[SOURce<HW>]:BB:C2K:MSTation:PRESet \n
		A standardized default for all the mobile stations (*RST values specified for the commands) . See 'Reset All Mobile
		Stations' for an overview. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BB:C2K:MSTation:PRESet')

	def preset_with_opc(self) -> None:
		"""[SOURce<HW>]:BB:C2K:MSTation:PRESet \n
		A standardized default for all the mobile stations (*RST values specified for the commands) . See 'Reset All Mobile
		Stations' for an overview. \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:C2K:MSTation:PRESet')
