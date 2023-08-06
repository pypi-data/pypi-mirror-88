from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.RepeatedCapability import RepeatedCapability
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Fblock:
	"""Fblock commands group definition. 222 total commands, 62 Sub-groups, 2 group commands
	Repeated Capability: Channel, default value after init: Channel.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("fblock", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_channel_get', 'repcap_channel_set', repcap.Channel.Nr1)

	def clone(self) -> 'Fblock':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Fblock(self._core, self._base.parent)
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
	def append(self):
		"""append commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_append'):
			from .Fblock_.Append import Append
			self._append = Append(self._core, self._base)
		return self._append

	@property
	def bchg(self):
		"""bchg commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bchg'):
			from .Fblock_.Bchg import Bchg
			self._bchg = Bchg(self._core, self._base)
		return self._bchg

	@property
	def bcSmoothing(self):
		"""bcSmoothing commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bcSmoothing'):
			from .Fblock_.BcSmoothing import BcSmoothing
			self._bcSmoothing = BcSmoothing(self._core, self._base)
		return self._bcSmoothing

	@property
	def bdcm(self):
		"""bdcm commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bdcm'):
			from .Fblock_.Bdcm import Bdcm
			self._bdcm = Bdcm(self._core, self._base)
		return self._bdcm

	@property
	def bfConfiguration(self):
		"""bfConfiguration commands group. 9 Sub-classes, 0 commands."""
		if not hasattr(self, '_bfConfiguration'):
			from .Fblock_.BfConfiguration import BfConfiguration
			self._bfConfiguration = BfConfiguration(self._core, self._base)
		return self._bfConfiguration

	@property
	def bmcs(self):
		"""bmcs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bmcs'):
			from .Fblock_.Bmcs import Bmcs
			self._bmcs = Bmcs(self._core, self._base)
		return self._bmcs

	@property
	def boost(self):
		"""boost commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_boost'):
			from .Fblock_.Boost import Boost
			self._boost = Boost(self._core, self._base)
		return self._boost

	@property
	def bssColor(self):
		"""bssColor commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bssColor'):
			from .Fblock_.BssColor import BssColor
			self._bssColor = BssColor(self._core, self._base)
		return self._bssColor

	@property
	def cbinonht(self):
		"""cbinonht commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cbinonht'):
			from .Fblock_.Cbinonht import Cbinonht
			self._cbinonht = Cbinonht(self._core, self._base)
		return self._cbinonht

	@property
	def cch1(self):
		"""cch1 commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_cch1'):
			from .Fblock_.Cch1 import Cch1
			self._cch1 = Cch1(self._core, self._base)
		return self._cch1

	@property
	def cch2(self):
		"""cch2 commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_cch2'):
			from .Fblock_.Cch2 import Cch2
			self._cch2 = Cch2(self._core, self._base)
		return self._cch2

	@property
	def cenru(self):
		"""cenru commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cenru'):
			from .Fblock_.Cenru import Cenru
			self._cenru = Cenru(self._core, self._base)
		return self._cenru

	@property
	def color(self):
		"""color commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_color'):
			from .Fblock_.Color import Color
			self._color = Color(self._core, self._base)
		return self._color

	@property
	def curpe(self):
		"""curpe commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_curpe'):
			from .Fblock_.Curpe import Curpe
			self._curpe = Curpe(self._core, self._base)
		return self._curpe

	@property
	def data(self):
		"""data commands group. 4 Sub-classes, 1 commands."""
		if not hasattr(self, '_data'):
			from .Fblock_.Data import Data
			self._data = Data(self._core, self._base)
		return self._data

	@property
	def dbinonht(self):
		"""dbinonht commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dbinonht'):
			from .Fblock_.Dbinonht import Dbinonht
			self._dbinonht = Dbinonht(self._core, self._base)
		return self._dbinonht

	@property
	def doppler(self):
		"""doppler commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_doppler'):
			from .Fblock_.Doppler import Doppler
			self._doppler = Doppler(self._core, self._base)
		return self._doppler

	@property
	def esStream(self):
		"""esStream commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_esStream'):
			from .Fblock_.EsStream import EsStream
			self._esStream = EsStream(self._core, self._base)
		return self._esStream

	@property
	def fcount(self):
		"""fcount commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fcount'):
			from .Fblock_.Fcount import Fcount
			self._fcount = Fcount(self._core, self._base)
		return self._fcount

	@property
	def guard(self):
		"""guard commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_guard'):
			from .Fblock_.Guard import Guard
			self._guard = Guard(self._core, self._base)
		return self._guard

	@property
	def insert(self):
		"""insert commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_insert'):
			from .Fblock_.Insert import Insert
			self._insert = Insert(self._core, self._base)
		return self._insert

	@property
	def itime(self):
		"""itime commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_itime'):
			from .Fblock_.Itime import Itime
			self._itime = Itime(self._core, self._base)
		return self._itime

	@property
	def link(self):
		"""link commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_link'):
			from .Fblock_.Link import Link
			self._link = Link(self._core, self._base)
		return self._link

	@property
	def logFile(self):
		"""logFile commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_logFile'):
			from .Fblock_.LogFile import LogFile
			self._logFile = LogFile(self._core, self._base)
		return self._logFile

	@property
	def logging(self):
		"""logging commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_logging'):
			from .Fblock_.Logging import Logging
			self._logging = Logging(self._core, self._base)
		return self._logging

	@property
	def mac(self):
		"""mac commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_mac'):
			from .Fblock_.Mac import Mac
			self._mac = Mac(self._core, self._base)
		return self._mac

	@property
	def maxPe(self):
		"""maxPe commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_maxPe'):
			from .Fblock_.MaxPe import MaxPe
			self._maxPe = MaxPe(self._core, self._base)
		return self._maxPe

	@property
	def mu(self):
		"""mu commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_mu'):
			from .Fblock_.Mu import Mu
			self._mu = Mu(self._core, self._base)
		return self._mu

	@property
	def muMimo(self):
		"""muMimo commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_muMimo'):
			from .Fblock_.MuMimo import MuMimo
			self._muMimo = MuMimo(self._core, self._base)
		return self._muMimo

	@property
	def ntps(self):
		"""ntps commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ntps'):
			from .Fblock_.Ntps import Ntps
			self._ntps = Ntps(self._core, self._base)
		return self._ntps

	@property
	def paid(self):
		"""paid commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_paid'):
			from .Fblock_.Paid import Paid
			self._paid = Paid(self._core, self._base)
		return self._paid

	@property
	def paste(self):
		"""paste commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_paste'):
			from .Fblock_.Paste import Paste
			self._paste = Paste(self._core, self._base)
		return self._paste

	@property
	def ped(self):
		"""ped commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ped'):
			from .Fblock_.Ped import Ped
			self._ped = Ped(self._core, self._base)
		return self._ped

	@property
	def pformat(self):
		"""pformat commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pformat'):
			from .Fblock_.Pformat import Pformat
			self._pformat = Pformat(self._core, self._base)
		return self._pformat

	@property
	def pfpFactor(self):
		"""pfpFactor commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pfpFactor'):
			from .Fblock_.PfpFactor import PfpFactor
			self._pfpFactor = PfpFactor(self._core, self._base)
		return self._pfpFactor

	@property
	def pitype(self):
		"""pitype commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pitype'):
			from .Fblock_.Pitype import Pitype
			self._pitype = Pitype(self._core, self._base)
		return self._pitype

	@property
	def plcp(self):
		"""plcp commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_plcp'):
			from .Fblock_.Plcp import Plcp
			self._plcp = Plcp(self._core, self._base)
		return self._plcp

	@property
	def pmode(self):
		"""pmode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pmode'):
			from .Fblock_.Pmode import Pmode
			self._pmode = Pmode(self._core, self._base)
		return self._pmode

	@property
	def ppuncturing(self):
		"""ppuncturing commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_ppuncturing'):
			from .Fblock_.Ppuncturing import Ppuncturing
			self._ppuncturing = Ppuncturing(self._core, self._base)
		return self._ppuncturing

	@property
	def preamble(self):
		"""preamble commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_preamble'):
			from .Fblock_.Preamble import Preamble
			self._preamble = Preamble(self._core, self._base)
		return self._preamble

	@property
	def prtype(self):
		"""prtype commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_prtype'):
			from .Fblock_.Prtype import Prtype
			self._prtype = Prtype(self._core, self._base)
		return self._prtype

	@property
	def psdu(self):
		"""psdu commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_psdu'):
			from .Fblock_.Psdu import Psdu
			self._psdu = Psdu(self._core, self._base)
		return self._psdu

	@property
	def right106Tone(self):
		"""right106Tone commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_right106Tone'):
			from .Fblock_.Right106Tone import Right106Tone
			self._right106Tone = Right106Tone(self._core, self._base)
		return self._right106Tone

	@property
	def segment(self):
		"""segment commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_segment'):
			from .Fblock_.Segment import Segment
			self._segment = Segment(self._core, self._base)
		return self._segment

	@property
	def smapping(self):
		"""smapping commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_smapping'):
			from .Fblock_.Smapping import Smapping
			self._smapping = Smapping(self._core, self._base)
		return self._smapping

	@property
	def smoothing(self):
		"""smoothing commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_smoothing'):
			from .Fblock_.Smoothing import Smoothing
			self._smoothing = Smoothing(self._core, self._base)
		return self._smoothing

	@property
	def spareUse(self):
		"""spareUse commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_spareUse'):
			from .Fblock_.SpareUse import SpareUse
			self._spareUse = SpareUse(self._core, self._base)
		return self._spareUse

	@property
	def sstream(self):
		"""sstream commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sstream'):
			from .Fblock_.Sstream import Sstream
			self._sstream = Sstream(self._core, self._base)
		return self._sstream

	@property
	def standard(self):
		"""standard commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_standard'):
			from .Fblock_.Standard import Standard
			self._standard = Standard(self._core, self._base)
		return self._standard

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Fblock_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def stbc(self):
		"""stbc commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_stbc'):
			from .Fblock_.Stbc import Stbc
			self._stbc = Stbc(self._core, self._base)
		return self._stbc

	@property
	def stStream(self):
		"""stStream commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_stStream'):
			from .Fblock_.StStream import StStream
			self._stStream = StStream(self._core, self._base)
		return self._stStream

	@property
	def symDuration(self):
		"""symDuration commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_symDuration'):
			from .Fblock_.SymDuration import SymDuration
			self._symDuration = SymDuration(self._core, self._base)
		return self._symDuration

	@property
	def tdWindowing(self):
		"""tdWindowing commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_tdWindowing'):
			from .Fblock_.TdWindowing import TdWindowing
			self._tdWindowing = TdWindowing(self._core, self._base)
		return self._tdWindowing

	@property
	def tmode(self):
		"""tmode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tmode'):
			from .Fblock_.Tmode import Tmode
			self._tmode = Tmode(self._core, self._base)
		return self._tmode

	@property
	def ttime(self):
		"""ttime commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ttime'):
			from .Fblock_.Ttime import Ttime
			self._ttime = Ttime(self._core, self._base)
		return self._ttime

	@property
	def txopDuration(self):
		"""txopDuration commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_txopDuration'):
			from .Fblock_.TxopDuration import TxopDuration
			self._txopDuration = TxopDuration(self._core, self._base)
		return self._txopDuration

	@property
	def typePy(self):
		"""typePy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_typePy'):
			from .Fblock_.TypePy import TypePy
			self._typePy = TypePy(self._core, self._base)
		return self._typePy

	@property
	def uindex(self):
		"""uindex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_uindex'):
			from .Fblock_.Uindex import Uindex
			self._uindex = Uindex(self._core, self._base)
		return self._uindex

	@property
	def uindication(self):
		"""uindication commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_uindication'):
			from .Fblock_.Uindication import Uindication
			self._uindication = Uindication(self._core, self._base)
		return self._uindication

	@property
	def ulen(self):
		"""ulen commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ulen'):
			from .Fblock_.Ulen import Ulen
			self._ulen = Ulen(self._core, self._base)
		return self._ulen

	@property
	def user(self):
		"""user commands group. 20 Sub-classes, 0 commands."""
		if not hasattr(self, '_user'):
			from .Fblock_.User import User
			self._user = User(self._core, self._base)
		return self._user

	def copy(self, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:COPY \n
		Copies the selected frame block. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:COPY')

	def copy_with_opc(self, channel=repcap.Channel.Default) -> None:
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:COPY \n
		Copies the selected frame block. \n
		Same as copy, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:COPY')

	def delete(self, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:DELete \n
		Deletes the selected frame block. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:DELete')

	def delete_with_opc(self, channel=repcap.Channel.Default) -> None:
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:DELete \n
		Deletes the selected frame block. \n
		Same as delete, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:DELete')
