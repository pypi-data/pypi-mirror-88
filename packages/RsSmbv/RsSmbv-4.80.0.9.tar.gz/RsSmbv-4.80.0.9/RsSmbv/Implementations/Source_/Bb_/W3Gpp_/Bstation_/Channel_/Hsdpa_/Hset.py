from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Hset:
	"""Hset commands group definition. 37 total commands, 29 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("hset", core, parent)

	def clone(self) -> 'Hset':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Hset(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def acLength(self):
		"""acLength commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_acLength'):
			from .Hset_.AcLength import AcLength
			self._acLength = AcLength(self._core, self._base)
		return self._acLength

	@property
	def altmodulation(self):
		"""altmodulation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_altmodulation'):
			from .Hset_.Altmodulation import Altmodulation
			self._altmodulation = Altmodulation(self._core, self._base)
		return self._altmodulation

	@property
	def amode(self):
		"""amode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_amode'):
			from .Hset_.Amode import Amode
			self._amode = Amode(self._core, self._base)
		return self._amode

	@property
	def bcbtti(self):
		"""bcbtti commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bcbtti'):
			from .Hset_.Bcbtti import Bcbtti
			self._bcbtti = Bcbtti(self._core, self._base)
		return self._bcbtti

	@property
	def bpayload(self):
		"""bpayload commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bpayload'):
			from .Hset_.Bpayload import Bpayload
			self._bpayload = Bpayload(self._core, self._base)
		return self._bpayload

	@property
	def clength(self):
		"""clength commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_clength'):
			from .Hset_.Clength import Clength
			self._clength = Clength(self._core, self._base)
		return self._clength

	@property
	def crate(self):
		"""crate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_crate'):
			from .Hset_.Crate import Crate
			self._crate = Crate(self._core, self._base)
		return self._crate

	@property
	def data(self):
		"""data commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_data'):
			from .Hset_.Data import Data
			self._data = Data(self._core, self._base)
		return self._data

	@property
	def harq(self):
		"""harq commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_harq'):
			from .Hset_.Harq import Harq
			self._harq = Harq(self._core, self._base)
		return self._harq

	@property
	def hscCode(self):
		"""hscCode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hscCode'):
			from .Hset_.HscCode import HscCode
			self._hscCode = HscCode(self._core, self._base)
		return self._hscCode

	@property
	def modulation(self):
		"""modulation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_modulation'):
			from .Hset_.Modulation import Modulation
			self._modulation = Modulation(self._core, self._base)
		return self._modulation

	@property
	def naiBitrate(self):
		"""naiBitrate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_naiBitrate'):
			from .Hset_.NaiBitrate import NaiBitrate
			self._naiBitrate = NaiBitrate(self._core, self._base)
		return self._naiBitrate

	@property
	def predefined(self):
		"""predefined commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_predefined'):
			from .Hset_.Predefined import Predefined
			self._predefined = Predefined(self._core, self._base)
		return self._predefined

	@property
	def pwPattern(self):
		"""pwPattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pwPattern'):
			from .Hset_.PwPattern import PwPattern
			self._pwPattern = PwPattern(self._core, self._base)
		return self._pwPattern

	@property
	def rvpSequence(self):
		"""rvpSequence commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rvpSequence'):
			from .Hset_.RvpSequence import RvpSequence
			self._rvpSequence = RvpSequence(self._core, self._base)
		return self._rvpSequence

	@property
	def rvParameter(self):
		"""rvParameter commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rvParameter'):
			from .Hset_.RvParameter import RvParameter
			self._rvParameter = RvParameter(self._core, self._base)
		return self._rvParameter

	@property
	def rvState(self):
		"""rvState commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rvState'):
			from .Hset_.RvState import RvState
			self._rvState = RvState(self._core, self._base)
		return self._rvState

	@property
	def s64Qam(self):
		"""s64Qam commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_s64Qam'):
			from .Hset_.S64Qam import S64Qam
			self._s64Qam = S64Qam(self._core, self._base)
		return self._s64Qam

	@property
	def scCode(self):
		"""scCode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scCode'):
			from .Hset_.ScCode import ScCode
			self._scCode = ScCode(self._core, self._base)
		return self._scCode

	@property
	def seed(self):
		"""seed commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_seed'):
			from .Hset_.Seed import Seed
			self._seed = Seed(self._core, self._base)
		return self._seed

	@property
	def slength(self):
		"""slength commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_slength'):
			from .Hset_.Slength import Slength
			self._slength = Slength(self._core, self._base)
		return self._slength

	@property
	def spattern(self):
		"""spattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_spattern'):
			from .Hset_.Spattern import Spattern
			self._spattern = Spattern(self._core, self._base)
		return self._spattern

	@property
	def staPattern(self):
		"""staPattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_staPattern'):
			from .Hset_.StaPattern import StaPattern
			self._staPattern = StaPattern(self._core, self._base)
		return self._staPattern

	@property
	def tbs(self):
		"""tbs commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_tbs'):
			from .Hset_.Tbs import Tbs
			self._tbs = Tbs(self._core, self._base)
		return self._tbs

	@property
	def tpower(self):
		"""tpower commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tpower'):
			from .Hset_.Tpower import Tpower
			self._tpower = Tpower(self._core, self._base)
		return self._tpower

	@property
	def typePy(self):
		"""typePy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_typePy'):
			from .Hset_.TypePy import TypePy
			self._typePy = TypePy(self._core, self._base)
		return self._typePy

	@property
	def ueCategory(self):
		"""ueCategory commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ueCategory'):
			from .Hset_.UeCategory import UeCategory
			self._ueCategory = UeCategory(self._core, self._base)
		return self._ueCategory

	@property
	def ueid(self):
		"""ueid commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ueid'):
			from .Hset_.Ueid import Ueid
			self._ueid = Ueid(self._core, self._base)
		return self._ueid

	@property
	def vibSize(self):
		"""vibSize commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_vibSize'):
			from .Hset_.VibSize import VibSize
			self._vibSize = VibSize(self._core, self._base)
		return self._vibSize

	def set(self, hset: int, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:BSTation<ST>:CHANnel<CH>:HSDPa:HSET \n
		No command help available \n
			:param hset: No help available
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')"""
		param = Conversions.decimal_value_to_str(hset)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:CHANnel{channel_cmd_val}:HSDPa:HSET {param}')

	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> int:
		"""[SOURce<HW>]:BB:W3GPp:BSTation<ST>:CHANnel<CH>:HSDPa:HSET \n
		No command help available \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')
			:return: hset: No help available"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:CHANnel{channel_cmd_val}:HSDPa:HSET?')
		return Conversions.str_to_int(response)

	def preset(self, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:BSTation<ST>:CHANnel:HSDPa:HSET:PRESet \n
		Sets the default settings of the channel table for the HSDPA H-Set mode. Channels 12 to 17 are preset for HSDPA H-Set 1. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:CHANnel:HSDPa:HSET:PRESet')

	def preset_with_opc(self, stream=repcap.Stream.Default) -> None:
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		"""[SOURce<HW>]:BB:W3GPp:BSTation<ST>:CHANnel:HSDPa:HSET:PRESet \n
		Sets the default settings of the channel table for the HSDPA H-Set mode. Channels 12 to 17 are preset for HSDPA H-Set 1. \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:CHANnel:HSDPa:HSET:PRESet')
