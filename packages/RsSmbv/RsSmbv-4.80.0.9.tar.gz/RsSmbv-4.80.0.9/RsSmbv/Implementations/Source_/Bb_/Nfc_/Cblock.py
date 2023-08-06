from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.RepeatedCapability import RepeatedCapability
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Cblock:
	"""Cblock commands group definition. 129 total commands, 107 Sub-groups, 2 group commands
	Repeated Capability: Channel, default value after init: Channel.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cblock", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_channel_get', 'repcap_channel_set', repcap.Channel.Nr1)

	def clone(self) -> 'Cblock':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Cblock(self._core, self._base.parent)
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
	def achk(self):
		"""achk commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_achk'):
			from .Cblock_.Achk import Achk
			self._achk = Achk(self._core, self._base)
		return self._achk

	@property
	def adata(self):
		"""adata commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_adata'):
			from .Cblock_.Adata import Adata
			self._adata = Adata(self._core, self._base)
		return self._adata

	@property
	def adCoding(self):
		"""adCoding commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_adCoding'):
			from .Cblock_.AdCoding import AdCoding
			self._adCoding = AdCoding(self._core, self._base)
		return self._adCoding

	@property
	def afi(self):
		"""afi commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_afi'):
			from .Cblock_.Afi import Afi
			self._afi = Afi(self._core, self._base)
		return self._afi

	@property
	def aid(self):
		"""aid commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_aid'):
			from .Cblock_.Aid import Aid
			self._aid = Aid(self._core, self._base)
		return self._aid

	@property
	def alength(self):
		"""alength commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_alength'):
			from .Cblock_.Alength import Alength
			self._alength = Alength(self._core, self._base)
		return self._alength

	@property
	def anSelection(self):
		"""anSelection commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_anSelection'):
			from .Cblock_.AnSelection import AnSelection
			self._anSelection = AnSelection(self._core, self._base)
		return self._anSelection

	@property
	def apfSupported(self):
		"""apfSupported commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_apfSupported'):
			from .Cblock_.ApfSupported import ApfSupported
			self._apfSupported = ApfSupported(self._core, self._base)
		return self._apfSupported

	@property
	def apGeneric(self):
		"""apGeneric commands group. 9 Sub-classes, 0 commands."""
		if not hasattr(self, '_apGeneric'):
			from .Cblock_.ApGeneric import ApGeneric
			self._apGeneric = ApGeneric(self._core, self._base)
		return self._apGeneric

	@property
	def append(self):
		"""append commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_append'):
			from .Cblock_.Append import Append
			self._append = Append(self._core, self._base)
		return self._append

	@property
	def atimeout(self):
		"""atimeout commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_atimeout'):
			from .Cblock_.Atimeout import Atimeout
			self._atimeout = Atimeout(self._core, self._base)
		return self._atimeout

	@property
	def aupd(self):
		"""aupd commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_aupd'):
			from .Cblock_.Aupd import Aupd
			self._aupd = Aupd(self._core, self._base)
		return self._aupd

	@property
	def bccError(self):
		"""bccError commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bccError'):
			from .Cblock_.BccError import BccError
			self._bccError = BccError(self._core, self._base)
		return self._bccError

	@property
	def bchk(self):
		"""bchk commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bchk'):
			from .Cblock_.Bchk import Bchk
			self._bchk = Bchk(self._core, self._base)
		return self._bchk

	@property
	def bfsdd(self):
		"""bfsdd commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bfsdd'):
			from .Cblock_.Bfsdd import Bfsdd
			self._bfsdd = Bfsdd(self._core, self._base)
		return self._bfsdd

	@property
	def blkSelection(self):
		"""blkSelection commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_blkSelection'):
			from .Cblock_.BlkSelection import BlkSelection
			self._blkSelection = BlkSelection(self._core, self._base)
		return self._blkSelection

	@property
	def block(self):
		"""block commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_block'):
			from .Cblock_.Block import Block
			self._block = Block(self._core, self._base)
		return self._block

	@property
	def bno(self):
		"""bno commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bno'):
			from .Cblock_.Bno import Bno
			self._bno = Bno(self._core, self._base)
		return self._bno

	@property
	def bpGeneric(self):
		"""bpGeneric commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_bpGeneric'):
			from .Cblock_.BpGeneric import BpGeneric
			self._bpGeneric = BpGeneric(self._core, self._base)
		return self._bpGeneric

	@property
	def btype(self):
		"""btype commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_btype'):
			from .Cblock_.Btype import Btype
			self._btype = Btype(self._core, self._base)
		return self._btype

	@property
	def bupd(self):
		"""bupd commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bupd'):
			from .Cblock_.Bupd import Bupd
			self._bupd = Bupd(self._core, self._base)
		return self._bupd

	@property
	def bytSelection(self):
		"""bytSelection commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bytSelection'):
			from .Cblock_.BytSelection import BytSelection
			self._bytSelection = BytSelection(self._core, self._base)
		return self._bytSelection

	@property
	def cfgType(self):
		"""cfgType commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cfgType'):
			from .Cblock_.CfgType import CfgType
			self._cfgType = CfgType(self._core, self._base)
		return self._cfgType

	@property
	def chaining(self):
		"""chaining commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_chaining'):
			from .Cblock_.Chaining import Chaining
			self._chaining = Chaining(self._core, self._base)
		return self._chaining

	@property
	def ctype(self):
		"""ctype commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ctype'):
			from .Cblock_.Ctype import Ctype
			self._ctype = Ctype(self._core, self._base)
		return self._ctype

	@property
	def data(self):
		"""data commands group. 3 Sub-classes, 1 commands."""
		if not hasattr(self, '_data'):
			from .Cblock_.Data import Data
			self._data = Data(self._core, self._base)
		return self._data

	@property
	def deqd(self):
		"""deqd commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_deqd'):
			from .Cblock_.Deqd import Deqd
			self._deqd = Deqd(self._core, self._base)
		return self._deqd

	@property
	def dfollowing(self):
		"""dfollowing commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dfollowing'):
			from .Cblock_.Dfollowing import Dfollowing
			self._dfollowing = Dfollowing(self._core, self._base)
		return self._dfollowing

	@property
	def did(self):
		"""did commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_did'):
			from .Cblock_.Did import Did
			self._did = Did(self._core, self._base)
		return self._did

	@property
	def dlp2(self):
		"""dlp2 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dlp2'):
			from .Cblock_.Dlp2 import Dlp2
			self._dlp2 = Dlp2(self._core, self._base)
		return self._dlp2

	@property
	def dlp4(self):
		"""dlp4 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dlp4'):
			from .Cblock_.Dlp4 import Dlp4
			self._dlp4 = Dlp4(self._core, self._base)
		return self._dlp4

	@property
	def dlp8(self):
		"""dlp8 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dlp8'):
			from .Cblock_.Dlp8 import Dlp8
			self._dlp8 = Dlp8(self._core, self._base)
		return self._dlp8

	@property
	def dltPoll(self):
		"""dltPoll commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dltPoll'):
			from .Cblock_.DltPoll import DltPoll
			self._dltPoll = DltPoll(self._core, self._base)
		return self._dltPoll

	@property
	def dpl2(self):
		"""dpl2 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dpl2'):
			from .Cblock_.Dpl2 import Dpl2
			self._dpl2 = Dpl2(self._core, self._base)
		return self._dpl2

	@property
	def dpl4(self):
		"""dpl4 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dpl4'):
			from .Cblock_.Dpl4 import Dpl4
			self._dpl4 = Dpl4(self._core, self._base)
		return self._dpl4

	@property
	def dpl8(self):
		"""dpl8 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dpl8'):
			from .Cblock_.Dpl8 import Dpl8
			self._dpl8 = Dpl8(self._core, self._base)
		return self._dpl8

	@property
	def dptListen(self):
		"""dptListen commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dptListen'):
			from .Cblock_.DptListen import DptListen
			self._dptListen = DptListen(self._core, self._base)
		return self._dptListen

	@property
	def dri(self):
		"""dri commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dri'):
			from .Cblock_.Dri import Dri
			self._dri = Dri(self._core, self._base)
		return self._dri

	@property
	def dsi(self):
		"""dsi commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dsi'):
			from .Cblock_.Dsi import Dsi
			self._dsi = Dsi(self._core, self._base)
		return self._dsi

	@property
	def dsupported(self):
		"""dsupported commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dsupported'):
			from .Cblock_.Dsupported import Dsupported
			self._dsupported = Dsupported(self._core, self._base)
		return self._dsupported

	@property
	def duration(self):
		"""duration commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_duration'):
			from .Cblock_.Duration import Duration
			self._duration = Duration(self._core, self._base)
		return self._duration

	@property
	def dwSelection(self):
		"""dwSelection commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dwSelection'):
			from .Cblock_.DwSelection import DwSelection
			self._dwSelection = DwSelection(self._core, self._base)
		return self._dwSelection

	@property
	def echk(self):
		"""echk commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_echk'):
			from .Cblock_.Echk import Echk
			self._echk = Echk(self._core, self._base)
		return self._echk

	@property
	def esSupported(self):
		"""esSupported commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_esSupported'):
			from .Cblock_.EsSupported import EsSupported
			self._esSupported = EsSupported(self._core, self._base)
		return self._esSupported

	@property
	def eupd(self):
		"""eupd commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_eupd'):
			from .Cblock_.Eupd import Eupd
			self._eupd = Eupd(self._core, self._base)
		return self._eupd

	@property
	def fpGeneric(self):
		"""fpGeneric commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_fpGeneric'):
			from .Cblock_.FpGeneric import FpGeneric
			self._fpGeneric = FpGeneric(self._core, self._base)
		return self._fpGeneric

	@property
	def fsc(self):
		"""fsc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fsc'):
			from .Cblock_.Fsc import Fsc
			self._fsc = Fsc(self._core, self._base)
		return self._fsc

	@property
	def fwi(self):
		"""fwi commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fwi'):
			from .Cblock_.Fwi import Fwi
			self._fwi = Fwi(self._core, self._base)
		return self._fwi

	@property
	def gbSelection(self):
		"""gbSelection commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_gbSelection'):
			from .Cblock_.GbSelection import GbSelection
			self._gbSelection = GbSelection(self._core, self._base)
		return self._gbSelection

	@property
	def gdAvailable(self):
		"""gdAvailable commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_gdAvailable'):
			from .Cblock_.GdAvailable import GdAvailable
			self._gdAvailable = GdAvailable(self._core, self._base)
		return self._gdAvailable

	@property
	def ibNumber(self):
		"""ibNumber commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ibNumber'):
			from .Cblock_.IbNumber import IbNumber
			self._ibNumber = IbNumber(self._core, self._base)
		return self._ibNumber

	@property
	def insert(self):
		"""insert commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_insert'):
			from .Cblock_.Insert import Insert
			self._insert = Insert(self._core, self._base)
		return self._insert

	@property
	def kparameter(self):
		"""kparameter commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_kparameter'):
			from .Cblock_.Kparameter import Kparameter
			self._kparameter = Kparameter(self._core, self._base)
		return self._kparameter

	@property
	def lreduction(self):
		"""lreduction commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_lreduction'):
			from .Cblock_.Lreduction import Lreduction
			self._lreduction = Lreduction(self._core, self._base)
		return self._lreduction

	@property
	def mbli(self):
		"""mbli commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mbli'):
			from .Cblock_.Mbli import Mbli
			self._mbli = Mbli(self._core, self._base)
		return self._mbli

	@property
	def miChaining(self):
		"""miChaining commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_miChaining'):
			from .Cblock_.MiChaining import MiChaining
			self._miChaining = MiChaining(self._core, self._base)
		return self._miChaining

	@property
	def mtr0(self):
		"""mtr0 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mtr0'):
			from .Cblock_.Mtr0 import Mtr0
			self._mtr0 = Mtr0(self._core, self._base)
		return self._mtr0

	@property
	def mtr1(self):
		"""mtr1 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mtr1'):
			from .Cblock_.Mtr1 import Mtr1
			self._mtr1 = Mtr1(self._core, self._base)
		return self._mtr1

	@property
	def mtr2(self):
		"""mtr2 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mtr2'):
			from .Cblock_.Mtr2 import Mtr2
			self._mtr2 = Mtr2(self._core, self._base)
		return self._mtr2

	@property
	def n2Ftype(self):
		"""n2Ftype commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_n2Ftype'):
			from .Cblock_.N2Ftype import N2Ftype
			self._n2Ftype = N2Ftype(self._core, self._base)
		return self._n2Ftype

	@property
	def nack(self):
		"""nack commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nack'):
			from .Cblock_.Nack import Nack
			self._nack = Nack(self._core, self._base)
		return self._nack

	@property
	def nad(self):
		"""nad commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nad'):
			from .Cblock_.Nad import Nad
			self._nad = Nad(self._core, self._base)
		return self._nad

	@property
	def nblocks(self):
		"""nblocks commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nblocks'):
			from .Cblock_.Nblocks import Nblocks
			self._nblocks = Nblocks(self._core, self._base)
		return self._nblocks

	@property
	def nfollowing(self):
		"""nfollowing commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nfollowing'):
			from .Cblock_.Nfollowing import Nfollowing
			self._nfollowing = Nfollowing(self._core, self._base)
		return self._nfollowing

	@property
	def nid0(self):
		"""nid0 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nid0'):
			from .Cblock_.Nid0 import Nid0
			self._nid0 = Nid0(self._core, self._base)
		return self._nid0

	@property
	def nid1(self):
		"""nid1 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nid1'):
			from .Cblock_.Nid1 import Nid1
			self._nid1 = Nid1(self._core, self._base)
		return self._nid1

	@property
	def nid2(self):
		"""nid2 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nid2'):
			from .Cblock_.Nid2 import Nid2
			self._nid2 = Nid2(self._core, self._base)
		return self._nid2

	@property
	def nnComplete(self):
		"""nnComplete commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nnComplete'):
			from .Cblock_.NnComplete import NnComplete
			self._nnComplete = NnComplete(self._core, self._base)
		return self._nnComplete

	@property
	def noApplications(self):
		"""noApplications commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_noApplications'):
			from .Cblock_.NoApplications import NoApplications
			self._noApplications = NoApplications(self._core, self._base)
		return self._noApplications

	@property
	def noSlots(self):
		"""noSlots commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_noSlots'):
			from .Cblock_.NoSlots import NoSlots
			self._noSlots = NoSlots(self._core, self._base)
		return self._noSlots

	@property
	def nservices(self):
		"""nservices commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nservices'):
			from .Cblock_.Nservices import Nservices
			self._nservices = Nservices(self._core, self._base)
		return self._nservices

	@property
	def nsize(self):
		"""nsize commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nsize'):
			from .Cblock_.Nsize import Nsize
			self._nsize = Nsize(self._core, self._base)
		return self._nsize

	@property
	def nsupported(self):
		"""nsupported commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nsupported'):
			from .Cblock_.Nsupported import Nsupported
			self._nsupported = Nsupported(self._core, self._base)
		return self._nsupported

	@property
	def pad0(self):
		"""pad0 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pad0'):
			from .Cblock_.Pad0 import Pad0
			self._pad0 = Pad0(self._core, self._base)
		return self._pad0

	@property
	def pad1(self):
		"""pad1 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pad1'):
			from .Cblock_.Pad1 import Pad1
			self._pad1 = Pad1(self._core, self._base)
		return self._pad1

	@property
	def pad2(self):
		"""pad2 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pad2'):
			from .Cblock_.Pad2 import Pad2
			self._pad2 = Pad2(self._core, self._base)
		return self._pad2

	@property
	def paste(self):
		"""paste commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_paste'):
			from .Cblock_.Paste import Paste
			self._paste = Paste(self._core, self._base)
		return self._paste

	@property
	def pduType(self):
		"""pduType commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pduType'):
			from .Cblock_.PduType import PduType
			self._pduType = PduType(self._core, self._base)
		return self._pduType

	@property
	def plin(self):
		"""plin commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_plin'):
			from .Cblock_.Plin import Plin
			self._plin = Plin(self._core, self._base)
		return self._plin

	@property
	def plir(self):
		"""plir commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_plir'):
			from .Cblock_.Plir import Plir
			self._plir = Plir(self._core, self._base)
		return self._plir

	@property
	def pni(self):
		"""pni commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pni'):
			from .Cblock_.Pni import Pni
			self._pni = Pni(self._core, self._base)
		return self._pni

	@property
	def poffset(self):
		"""poffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_poffset'):
			from .Cblock_.Poffset import Poffset
			self._poffset = Poffset(self._core, self._base)
		return self._poffset

	@property
	def pselection(self):
		"""pselection commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pselection'):
			from .Cblock_.Pselection import Pselection
			self._pselection = Pselection(self._core, self._base)
		return self._pselection

	@property
	def rc(self):
		"""rc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rc'):
			from .Cblock_.Rc import Rc
			self._rc = Rc(self._core, self._base)
		return self._rc

	@property
	def repetition(self):
		"""repetition commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_repetition'):
			from .Cblock_.Repetition import Repetition
			self._repetition = Repetition(self._core, self._base)
		return self._repetition

	@property
	def rtox(self):
		"""rtox commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rtox'):
			from .Cblock_.Rtox import Rtox
			self._rtox = Rtox(self._core, self._base)
		return self._rtox

	@property
	def samples(self):
		"""samples commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_samples'):
			from .Cblock_.Samples import Samples
			self._samples = Samples(self._core, self._base)
		return self._samples

	@property
	def scmd(self):
		"""scmd commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scmd'):
			from .Cblock_.Scmd import Scmd
			self._scmd = Scmd(self._core, self._base)
		return self._scmd

	@property
	def scode(self):
		"""scode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scode'):
			from .Cblock_.Scode import Scode
			self._scode = Scode(self._core, self._base)
		return self._scode

	@property
	def segSelection(self):
		"""segSelection commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_segSelection'):
			from .Cblock_.SegSelection import SegSelection
			self._segSelection = SegSelection(self._core, self._base)
		return self._segSelection

	@property
	def senrequired(self):
		"""senrequired commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_senrequired'):
			from .Cblock_.Senrequired import Senrequired
			self._senrequired = Senrequired(self._core, self._base)
		return self._senrequired

	@property
	def service(self):
		"""service commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_service'):
			from .Cblock_.Service import Service
			self._service = Service(self._core, self._base)
		return self._service

	@property
	def sf1(self):
		"""sf1 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sf1'):
			from .Cblock_.Sf1 import Sf1
			self._sf1 = Sf1(self._core, self._base)
		return self._sf1

	@property
	def sf2(self):
		"""sf2 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sf2'):
			from .Cblock_.Sf2 import Sf2
			self._sf2 = Sf2(self._core, self._base)
		return self._sf2

	@property
	def sfgi(self):
		"""sfgi commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sfgi'):
			from .Cblock_.Sfgi import Sfgi
			self._sfgi = Sfgi(self._core, self._base)
		return self._sfgi

	@property
	def sno(self):
		"""sno commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sno'):
			from .Cblock_.Sno import Sno
			self._sno = Sno(self._core, self._base)
		return self._sno

	@property
	def snumber(self):
		"""snumber commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_snumber'):
			from .Cblock_.Snumber import Snumber
			self._snumber = Snumber(self._core, self._base)
		return self._snumber

	@property
	def spLower(self):
		"""spLower commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_spLower'):
			from .Cblock_.SpLower import SpLower
			self._spLower = SpLower(self._core, self._base)
		return self._spLower

	@property
	def spUpper(self):
		"""spUpper commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_spUpper'):
			from .Cblock_.SpUpper import SpUpper
			self._spUpper = SpUpper(self._core, self._base)
		return self._spUpper

	@property
	def ssnRequired(self):
		"""ssnRequired commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ssnRequired'):
			from .Cblock_.SsnRequired import SsnRequired
			self._ssnRequired = SsnRequired(self._core, self._base)
		return self._ssnRequired

	@property
	def stime(self):
		"""stime commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_stime'):
			from .Cblock_.Stime import Stime
			self._stime = Stime(self._core, self._base)
		return self._stime

	@property
	def t1Tconfigured(self):
		"""t1Tconfigured commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_t1Tconfigured'):
			from .Cblock_.T1Tconfigured import T1Tconfigured
			self._t1Tconfigured = T1Tconfigured(self._core, self._base)
		return self._t1Tconfigured

	@property
	def t1Tk(self):
		"""t1Tk commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_t1Tk'):
			from .Cblock_.T1Tk import T1Tk
			self._t1Tk = T1Tk(self._core, self._base)
		return self._t1Tk

	@property
	def taipicc(self):
		"""taipicc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_taipicc'):
			from .Cblock_.Taipicc import Taipicc
			self._taipicc = Taipicc(self._core, self._base)
		return self._taipicc

	@property
	def tsn(self):
		"""tsn commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tsn'):
			from .Cblock_.Tsn import Tsn
			self._tsn = Tsn(self._core, self._base)
		return self._tsn

	@property
	def wt(self):
		"""wt commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_wt'):
			from .Cblock_.Wt import Wt
			self._wt = Wt(self._core, self._base)
		return self._wt

	@property
	def wtxm(self):
		"""wtxm commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_wtxm'):
			from .Cblock_.Wtxm import Wtxm
			self._wtxm = Wtxm(self._core, self._base)
		return self._wtxm

	def copy(self, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:NFC:CBLock<CH>:COPY \n
		Copies a command block for later use. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:COPY')

	def copy_with_opc(self, channel=repcap.Channel.Default) -> None:
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		"""[SOURce<HW>]:BB:NFC:CBLock<CH>:COPY \n
		Copies a command block for later use. \n
		Same as copy, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:COPY')

	def delete(self, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:NFC:CBLock<CH>:DELete \n
		Removes a command block from the command sequence. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:DELete')

	def delete_with_opc(self, channel=repcap.Channel.Default) -> None:
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		"""[SOURce<HW>]:BB:NFC:CBLock<CH>:DELete \n
		Removes a command block from the command sequence. \n
		Same as delete, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:DELete')
