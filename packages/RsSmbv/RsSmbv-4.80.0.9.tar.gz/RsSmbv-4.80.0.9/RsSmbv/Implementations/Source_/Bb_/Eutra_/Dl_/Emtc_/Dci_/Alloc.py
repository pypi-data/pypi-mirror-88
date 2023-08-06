from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.RepeatedCapability import RepeatedCapability
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Alloc:
	"""Alloc commands group definition. 42 total commands, 42 Sub-groups, 0 group commands
	Repeated Capability: Channel, default value after init: Channel.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("alloc", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_channel_get', 'repcap_channel_set', repcap.Channel.Nr1)

	def clone(self) -> 'Alloc':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Alloc(self._core, self._base.parent)
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
	def apsi(self):
		"""apsi commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_apsi'):
			from .Alloc_.Apsi import Apsi
			self._apsi = Apsi(self._core, self._base)
		return self._apsi

	@property
	def bits(self):
		"""bits commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bits'):
			from .Alloc_.Bits import Bits
			self._bits = Bits(self._core, self._base)
		return self._bits

	@property
	def cces(self):
		"""cces commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cces'):
			from .Alloc_.Cces import Cces
			self._cces = Cces(self._core, self._base)
		return self._cces

	@property
	def conflict(self):
		"""conflict commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_conflict'):
			from .Alloc_.Conflict import Conflict
			self._conflict = Conflict(self._core, self._base)
		return self._conflict

	@property
	def csiRequest(self):
		"""csiRequest commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_csiRequest'):
			from .Alloc_.CsiRequest import CsiRequest
			self._csiRequest = CsiRequest(self._core, self._base)
		return self._csiRequest

	@property
	def daIndex(self):
		"""daIndex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_daIndex'):
			from .Alloc_.DaIndex import DaIndex
			self._daIndex = DaIndex(self._core, self._base)
		return self._daIndex

	@property
	def diInfo(self):
		"""diInfo commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_diInfo'):
			from .Alloc_.DiInfo import DiInfo
			self._diInfo = DiInfo(self._core, self._base)
		return self._diInfo

	@property
	def fmt(self):
		"""fmt commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fmt'):
			from .Alloc_.Fmt import Fmt
			self._fmt = Fmt(self._core, self._base)
		return self._fmt

	@property
	def harq(self):
		"""harq commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_harq'):
			from .Alloc_.Harq import Harq
			self._harq = Harq(self._core, self._base)
		return self._harq

	@property
	def hresOffset(self):
		"""hresOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hresOffset'):
			from .Alloc_.HresOffset import HresOffset
			self._hresOffset = HresOffset(self._core, self._base)
		return self._hresOffset

	@property
	def idcce(self):
		"""idcce commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_idcce'):
			from .Alloc_.Idcce import Idcce
			self._idcce = Idcce(self._core, self._base)
		return self._idcce

	@property
	def mcs(self):
		"""mcs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mcs'):
			from .Alloc_.Mcs import Mcs
			self._mcs = Mcs(self._core, self._base)
		return self._mcs

	@property
	def mpdcchset(self):
		"""mpdcchset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mpdcchset'):
			from .Alloc_.Mpdcchset import Mpdcchset
			self._mpdcchset = Mpdcchset(self._core, self._base)
		return self._mpdcchset

	@property
	def ndcces(self):
		"""ndcces commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ndcces'):
			from .Alloc_.Ndcces import Ndcces
			self._ndcces = Ndcces(self._core, self._base)
		return self._ndcces

	@property
	def ndind(self):
		"""ndind commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ndind'):
			from .Alloc_.Ndind import Ndind
			self._ndind = Ndind(self._core, self._base)
		return self._ndind

	@property
	def nrep(self):
		"""nrep commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nrep'):
			from .Alloc_.Nrep import Nrep
			self._nrep = Nrep(self._core, self._base)
		return self._nrep

	@property
	def pagng(self):
		"""pagng commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pagng'):
			from .Alloc_.Pagng import Pagng
			self._pagng = Pagng(self._core, self._base)
		return self._pagng

	@property
	def pdcch(self):
		"""pdcch commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pdcch'):
			from .Alloc_.Pdcch import Pdcch
			self._pdcch = Pdcch(self._core, self._base)
		return self._pdcch

	@property
	def pdsHopping(self):
		"""pdsHopping commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pdsHopping'):
			from .Alloc_.PdsHopping import PdsHopping
			self._pdsHopping = PdsHopping(self._core, self._base)
		return self._pdsHopping

	@property
	def pfrHopp(self):
		"""pfrHopp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pfrHopp'):
			from .Alloc_.PfrHopp import PfrHopp
			self._pfrHopp = PfrHopp(self._core, self._base)
		return self._pfrHopp

	@property
	def pmiConfirm(self):
		"""pmiConfirm commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pmiConfirm'):
			from .Alloc_.PmiConfirm import PmiConfirm
			self._pmiConfirm = PmiConfirm(self._core, self._base)
		return self._pmiConfirm

	@property
	def praMask(self):
		"""praMask commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_praMask'):
			from .Alloc_.PraMask import PraMask
			self._praMask = PraMask(self._core, self._base)
		return self._praMask

	@property
	def praPreamble(self):
		"""praPreamble commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_praPreamble'):
			from .Alloc_.PraPreamble import PraPreamble
			self._praPreamble = PraPreamble(self._core, self._base)
		return self._praPreamble

	@property
	def praStart(self):
		"""praStart commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_praStart'):
			from .Alloc_.PraStart import PraStart
			self._praStart = PraStart(self._core, self._base)
		return self._praStart

	@property
	def rba(self):
		"""rba commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rba'):
			from .Alloc_.Rba import Rba
			self._rba = Rba(self._core, self._base)
		return self._rba

	@property
	def rbaf(self):
		"""rbaf commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rbaf'):
			from .Alloc_.Rbaf import Rbaf
			self._rbaf = Rbaf(self._core, self._base)
		return self._rbaf

	@property
	def repmpdcch(self):
		"""repmpdcch commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_repmpdcch'):
			from .Alloc_.Repmpdcch import Repmpdcch
			self._repmpdcch = Repmpdcch(self._core, self._base)
		return self._repmpdcch

	@property
	def reppdsch(self):
		"""reppdsch commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_reppdsch'):
			from .Alloc_.Reppdsch import Reppdsch
			self._reppdsch = Reppdsch(self._core, self._base)
		return self._reppdsch

	@property
	def rver(self):
		"""rver commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rver'):
			from .Alloc_.Rver import Rver
			self._rver = Rver(self._core, self._base)
		return self._rver

	@property
	def sfrNumber(self):
		"""sfrNumber commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sfrNumber'):
			from .Alloc_.SfrNumber import SfrNumber
			self._sfrNumber = SfrNumber(self._core, self._base)
		return self._sfrNumber

	@property
	def srsRequest(self):
		"""srsRequest commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_srsRequest'):
			from .Alloc_.SrsRequest import SrsRequest
			self._srsRequest = SrsRequest(self._core, self._base)
		return self._srsRequest

	@property
	def ssp(self):
		"""ssp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ssp'):
			from .Alloc_.Ssp import Ssp
			self._ssp = Ssp(self._core, self._base)
		return self._ssp

	@property
	def strv(self):
		"""strv commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_strv'):
			from .Alloc_.Strv import Strv
			self._strv = Strv(self._core, self._base)
		return self._strv

	@property
	def stsFrame(self):
		"""stsFrame commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_stsFrame'):
			from .Alloc_.StsFrame import StsFrame
			self._stsFrame = StsFrame(self._core, self._base)
		return self._stsFrame

	@property
	def tbs(self):
		"""tbs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tbs'):
			from .Alloc_.Tbs import Tbs
			self._tbs = Tbs(self._core, self._base)
		return self._tbs

	@property
	def tcmd(self):
		"""tcmd commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tcmd'):
			from .Alloc_.Tcmd import Tcmd
			self._tcmd = Tcmd(self._core, self._base)
		return self._tcmd

	@property
	def tpcpusch(self):
		"""tpcpusch commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tpcpusch'):
			from .Alloc_.Tpcpusch import Tpcpusch
			self._tpcpusch = Tpcpusch(self._core, self._base)
		return self._tpcpusch

	@property
	def tpmprec(self):
		"""tpmprec commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tpmprec'):
			from .Alloc_.Tpmprec import Tpmprec
			self._tpmprec = Tpmprec(self._core, self._base)
		return self._tpmprec

	@property
	def ueid(self):
		"""ueid commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ueid'):
			from .Alloc_.Ueid import Ueid
			self._ueid = Ueid(self._core, self._base)
		return self._ueid

	@property
	def ueMode(self):
		"""ueMode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ueMode'):
			from .Alloc_.UeMode import UeMode
			self._ueMode = UeMode(self._core, self._base)
		return self._ueMode

	@property
	def ulIndex(self):
		"""ulIndex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ulIndex'):
			from .Alloc_.UlIndex import UlIndex
			self._ulIndex = UlIndex(self._core, self._base)
		return self._ulIndex

	@property
	def user(self):
		"""user commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_user'):
			from .Alloc_.User import User
			self._user = User(self._core, self._base)
		return self._user
