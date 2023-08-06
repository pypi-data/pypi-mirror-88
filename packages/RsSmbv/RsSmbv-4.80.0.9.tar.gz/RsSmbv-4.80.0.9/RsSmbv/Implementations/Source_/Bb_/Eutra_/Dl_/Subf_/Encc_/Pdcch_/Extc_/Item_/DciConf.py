from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DciConf:
	"""DciConf commands group definition. 42 total commands, 37 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dciConf", core, parent)

	def clone(self) -> 'DciConf':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = DciConf(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def apLayer(self):
		"""apLayer commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_apLayer'):
			from .DciConf_.ApLayer import ApLayer
			self._apLayer = ApLayer(self._core, self._base)
		return self._apLayer

	@property
	def bitData(self):
		"""bitData commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bitData'):
			from .DciConf_.BitData import BitData
			self._bitData = BitData(self._core, self._base)
		return self._bitData

	@property
	def ciField(self):
		"""ciField commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ciField'):
			from .DciConf_.CiField import CiField
			self._ciField = CiField(self._core, self._base)
		return self._ciField

	@property
	def cqiRequest(self):
		"""cqiRequest commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cqiRequest'):
			from .DciConf_.CqiRequest import CqiRequest
			self._cqiRequest = CqiRequest(self._core, self._base)
		return self._cqiRequest

	@property
	def csdmrs(self):
		"""csdmrs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_csdmrs'):
			from .DciConf_.Csdmrs import Csdmrs
			self._csdmrs = Csdmrs(self._core, self._base)
		return self._csdmrs

	@property
	def csiRequest(self):
		"""csiRequest commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_csiRequest'):
			from .DciConf_.CsiRequest import CsiRequest
			self._csiRequest = CsiRequest(self._core, self._base)
		return self._csiRequest

	@property
	def dlaIndex(self):
		"""dlaIndex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dlaIndex'):
			from .DciConf_.DlaIndex import DlaIndex
			self._dlaIndex = DlaIndex(self._core, self._base)
		return self._dlaIndex

	@property
	def dpOffset(self):
		"""dpOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dpOffset'):
			from .DciConf_.DpOffset import DpOffset
			self._dpOffset = DpOffset(self._core, self._base)
		return self._dpOffset

	@property
	def f1Amode(self):
		"""f1Amode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_f1Amode'):
			from .DciConf_.F1Amode import F1Amode
			self._f1Amode = F1Amode(self._core, self._base)
		return self._f1Amode

	@property
	def gap(self):
		"""gap commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_gap'):
			from .DciConf_.Gap import Gap
			self._gap = Gap(self._core, self._base)
		return self._gap

	@property
	def hack(self):
		"""hack commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hack'):
			from .DciConf_.Hack import Hack
			self._hack = Hack(self._core, self._base)
		return self._hack

	@property
	def hpn(self):
		"""hpn commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hpn'):
			from .DciConf_.Hpn import Hpn
			self._hpn = Hpn(self._core, self._base)
		return self._hpn

	@property
	def laaSubframe(self):
		"""laaSubframe commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_laaSubframe'):
			from .DciConf_.LaaSubframe import LaaSubframe
			self._laaSubframe = LaaSubframe(self._core, self._base)
		return self._laaSubframe

	@property
	def mcsr(self):
		"""mcsr commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mcsr'):
			from .DciConf_.Mcsr import Mcsr
			self._mcsr = Mcsr(self._core, self._base)
		return self._mcsr

	@property
	def ndi(self):
		"""ndi commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ndi'):
			from .DciConf_.Ndi import Ndi
			self._ndi = Ndi(self._core, self._base)
		return self._ndi

	@property
	def pdre(self):
		"""pdre commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pdre'):
			from .DciConf_.Pdre import Pdre
			self._pdre = Pdre(self._core, self._base)
		return self._pdre

	@property
	def pfHopping(self):
		"""pfHopping commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pfHopping'):
			from .DciConf_.PfHopping import PfHopping
			self._pfHopping = PfHopping(self._core, self._base)
		return self._pfHopping

	@property
	def pmi(self):
		"""pmi commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pmi'):
			from .DciConf_.Pmi import Pmi
			self._pmi = Pmi(self._core, self._base)
		return self._pmi

	@property
	def prach(self):
		"""prach commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_prach'):
			from .DciConf_.Prach import Prach
			self._prach = Prach(self._core, self._base)
		return self._prach

	@property
	def precInfo(self):
		"""precInfo commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_precInfo'):
			from .DciConf_.PrecInfo import PrecInfo
			self._precInfo = PrecInfo(self._core, self._base)
		return self._precInfo

	@property
	def rah(self):
		"""rah commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rah'):
			from .DciConf_.Rah import Rah
			self._rah = Rah(self._core, self._base)
		return self._rah

	@property
	def rahr(self):
		"""rahr commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rahr'):
			from .DciConf_.Rahr import Rahr
			self._rahr = Rahr(self._core, self._base)
		return self._rahr

	@property
	def ratype(self):
		"""ratype commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ratype'):
			from .DciConf_.Ratype import Ratype
			self._ratype = Ratype(self._core, self._base)
		return self._ratype

	@property
	def rba(self):
		"""rba commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rba'):
			from .DciConf_.Rba import Rba
			self._rba = Rba(self._core, self._base)
		return self._rba

	@property
	def rv(self):
		"""rv commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rv'):
			from .DciConf_.Rv import Rv
			self._rv = Rv(self._core, self._base)
		return self._rv

	@property
	def sid(self):
		"""sid commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sid'):
			from .DciConf_.Sid import Sid
			self._sid = Sid(self._core, self._base)
		return self._sid

	@property
	def srsRequest(self):
		"""srsRequest commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_srsRequest'):
			from .DciConf_.SrsRequest import SrsRequest
			self._srsRequest = SrsRequest(self._core, self._base)
		return self._srsRequest

	@property
	def swapFlag(self):
		"""swapFlag commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_swapFlag'):
			from .DciConf_.SwapFlag import SwapFlag
			self._swapFlag = SwapFlag(self._core, self._base)
		return self._swapFlag

	@property
	def tb1(self):
		"""tb1 commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_tb1'):
			from .DciConf_.Tb1 import Tb1
			self._tb1 = Tb1(self._core, self._base)
		return self._tb1

	@property
	def tb2(self):
		"""tb2 commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_tb2'):
			from .DciConf_.Tb2 import Tb2
			self._tb2 = Tb2(self._core, self._base)
		return self._tb2

	@property
	def tbsi(self):
		"""tbsi commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tbsi'):
			from .DciConf_.Tbsi import Tbsi
			self._tbsi = Tbsi(self._core, self._base)
		return self._tbsi

	@property
	def tpcc(self):
		"""tpcc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tpcc'):
			from .DciConf_.Tpcc import Tpcc
			self._tpcc = Tpcc(self._core, self._base)
		return self._tpcc

	@property
	def tpcInstr(self):
		"""tpcInstr commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tpcInstr'):
			from .DciConf_.TpcInstr import TpcInstr
			self._tpcInstr = TpcInstr(self._core, self._base)
		return self._tpcInstr

	@property
	def tpmi(self):
		"""tpmi commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tpmi'):
			from .DciConf_.Tpmi import Tpmi
			self._tpmi = Tpmi(self._core, self._base)
		return self._tpmi

	@property
	def ulDlConf(self):
		"""ulDlConf commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ulDlConf'):
			from .DciConf_.UlDlConf import UlDlConf
			self._ulDlConf = UlDlConf(self._core, self._base)
		return self._ulDlConf

	@property
	def ulIndex(self):
		"""ulIndex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ulIndex'):
			from .DciConf_.UlIndex import UlIndex
			self._ulIndex = UlIndex(self._core, self._base)
		return self._ulIndex

	@property
	def vrba(self):
		"""vrba commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_vrba'):
			from .DciConf_.Vrba import Vrba
			self._vrba = Vrba(self._core, self._base)
		return self._vrba
