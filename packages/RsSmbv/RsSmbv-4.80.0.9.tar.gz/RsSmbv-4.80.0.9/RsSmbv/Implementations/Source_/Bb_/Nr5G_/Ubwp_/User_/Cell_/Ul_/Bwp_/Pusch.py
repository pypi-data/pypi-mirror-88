from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pusch:
	"""Pusch commands group definition. 61 total commands, 15 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pusch", core, parent)

	def clone(self) -> 'Pusch':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Pusch(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def cbSubset(self):
		"""cbSubset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cbSubset'):
			from .Pusch_.CbSubset import CbSubset
			self._cbSubset = CbSubset(self._core, self._base)
		return self._cbSubset

	@property
	def dmta(self):
		"""dmta commands group. 8 Sub-classes, 0 commands."""
		if not hasattr(self, '_dmta'):
			from .Pusch_.Dmta import Dmta
			self._dmta = Dmta(self._core, self._base)
		return self._dmta

	@property
	def dmtb(self):
		"""dmtb commands group. 7 Sub-classes, 0 commands."""
		if not hasattr(self, '_dmtb'):
			from .Pusch_.Dmtb import Dmtb
			self._dmtb = Dmtb(self._core, self._base)
		return self._dmtb

	@property
	def dsid(self):
		"""dsid commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dsid'):
			from .Pusch_.Dsid import Dsid
			self._dsid = Dsid(self._core, self._base)
		return self._dsid

	@property
	def fhOffsets(self):
		"""fhOffsets commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_fhOffsets'):
			from .Pusch_.FhOffsets import FhOffsets
			self._fhOffsets = FhOffsets(self._core, self._base)
		return self._fhOffsets

	@property
	def fhOp(self):
		"""fhOp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fhOp'):
			from .Pusch_.FhOp import FhOp
			self._fhOp = FhOp(self._core, self._base)
		return self._fhOp

	@property
	def mcbGroups(self):
		"""mcbGroups commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mcbGroups'):
			from .Pusch_.McbGroups import McbGroups
			self._mcbGroups = McbGroups(self._core, self._base)
		return self._mcbGroups

	@property
	def mcsTable(self):
		"""mcsTable commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mcsTable'):
			from .Pusch_.McsTable import McsTable
			self._mcsTable = McsTable(self._core, self._base)
		return self._mcsTable

	@property
	def mrank(self):
		"""mrank commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mrank'):
			from .Pusch_.Mrank import Mrank
			self._mrank = Mrank(self._core, self._base)
		return self._mrank

	@property
	def mttPrecoding(self):
		"""mttPrecoding commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mttPrecoding'):
			from .Pusch_.MttPrecoding import MttPrecoding
			self._mttPrecoding = MttPrecoding(self._core, self._base)
		return self._mttPrecoding

	@property
	def rbgSize(self):
		"""rbgSize commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rbgSize'):
			from .Pusch_.RbgSize import RbgSize
			self._rbgSize = RbgSize(self._core, self._base)
		return self._rbgSize

	@property
	def resAlloc(self):
		"""resAlloc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_resAlloc'):
			from .Pusch_.ResAlloc import ResAlloc
			self._resAlloc = ResAlloc(self._core, self._base)
		return self._resAlloc

	@property
	def scrambling(self):
		"""scrambling commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_scrambling'):
			from .Pusch_.Scrambling import Scrambling
			self._scrambling = Scrambling(self._core, self._base)
		return self._scrambling

	@property
	def tpState(self):
		"""tpState commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tpState'):
			from .Pusch_.TpState import TpState
			self._tpState = TpState(self._core, self._base)
		return self._tpState

	@property
	def txConfig(self):
		"""txConfig commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_txConfig'):
			from .Pusch_.TxConfig import TxConfig
			self._txConfig = TxConfig(self._core, self._base)
		return self._txConfig
