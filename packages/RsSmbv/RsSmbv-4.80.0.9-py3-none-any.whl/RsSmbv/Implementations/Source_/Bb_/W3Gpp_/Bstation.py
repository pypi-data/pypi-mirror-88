from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.RepeatedCapability import RepeatedCapability
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Bstation:
	"""Bstation commands group definition. 170 total commands, 13 Sub-groups, 1 group commands
	Repeated Capability: Stream, default value after init: Stream.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("bstation", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_stream_get', 'repcap_stream_set', repcap.Stream.Nr1)

	def clone(self) -> 'Bstation':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Bstation(self._core, self._base.parent)
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
	def channel(self):
		"""channel commands group. 14 Sub-classes, 1 commands."""
		if not hasattr(self, '_channel'):
			from .Bstation_.Channel import Channel
			self._channel = Channel(self._core, self._base)
		return self._channel

	@property
	def cmode(self):
		"""cmode commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_cmode'):
			from .Bstation_.Cmode import Cmode
			self._cmode = Cmode(self._core, self._base)
		return self._cmode

	@property
	def dconflict(self):
		"""dconflict commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_dconflict'):
			from .Bstation_.Dconflict import Dconflict
			self._dconflict = Dconflict(self._core, self._base)
		return self._dconflict

	@property
	def enhanced(self):
		"""enhanced commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_enhanced'):
			from .Bstation_.Enhanced import Enhanced
			self._enhanced = Enhanced(self._core, self._base)
		return self._enhanced

	@property
	def ocns(self):
		"""ocns commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_ocns'):
			from .Bstation_.Ocns import Ocns
			self._ocns = Ocns(self._core, self._base)
		return self._ocns

	@property
	def oltDiversity(self):
		"""oltDiversity commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_oltDiversity'):
			from .Bstation_.OltDiversity import OltDiversity
			self._oltDiversity = OltDiversity(self._core, self._base)
		return self._oltDiversity

	@property
	def pindicator(self):
		"""pindicator commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_pindicator'):
			from .Bstation_.Pindicator import Pindicator
			self._pindicator = Pindicator(self._core, self._base)
		return self._pindicator

	@property
	def scode(self):
		"""scode commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_scode'):
			from .Bstation_.Scode import Scode
			self._scode = Scode(self._core, self._base)
		return self._scode

	@property
	def scpich(self):
		"""scpich commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_scpich'):
			from .Bstation_.Scpich import Scpich
			self._scpich = Scpich(self._core, self._base)
		return self._scpich

	@property
	def sscg(self):
		"""sscg commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sscg'):
			from .Bstation_.Sscg import Sscg
			self._sscg = Sscg(self._core, self._base)
		return self._sscg

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Bstation_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def tdelay(self):
		"""tdelay commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tdelay'):
			from .Bstation_.Tdelay import Tdelay
			self._tdelay = Tdelay(self._core, self._base)
		return self._tdelay

	@property
	def tdiversity(self):
		"""tdiversity commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tdiversity'):
			from .Bstation_.Tdiversity import Tdiversity
			self._tdiversity = Tdiversity(self._core, self._base)
		return self._tdiversity

	def preset(self) -> None:
		"""[SOURce<HW>]:BB:W3GPp:BSTation:PRESet \n
		The command produces a standardized default for all the base stations. The settings correspond to the *RST values
		specified for the commands. All base station settings are preset. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:BSTation:PRESet')

	def preset_with_opc(self) -> None:
		"""[SOURce<HW>]:BB:W3GPp:BSTation:PRESet \n
		The command produces a standardized default for all the base stations. The settings correspond to the *RST values
		specified for the commands. All base station settings are preset. \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:W3GPp:BSTation:PRESet')
