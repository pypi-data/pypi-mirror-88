from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pusch:
	"""Pusch commands group definition. 40 total commands, 11 Sub-groups, 0 group commands"""

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
	def bmaid(self):
		"""bmaid commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bmaid'):
			from .Pusch_.Bmaid import Bmaid
			self._bmaid = Bmaid(self._core, self._base)
		return self._bmaid

	@property
	def dmr(self):
		"""dmr commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_dmr'):
			from .Pusch_.Dmr import Dmr
			self._dmr = Dmr(self._core, self._base)
		return self._dmr

	@property
	def dmrs(self):
		"""dmrs commands group. 7 Sub-classes, 0 commands."""
		if not hasattr(self, '_dmrs'):
			from .Pusch_.Dmrs import Dmrs
			self._dmrs = Dmrs(self._core, self._base)
		return self._dmrs

	@property
	def fhOi(self):
		"""fhOi commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fhOi'):
			from .Pusch_.FhOi import FhOi
			self._fhOi = FhOi(self._core, self._base)
		return self._fhOi

	@property
	def fhOp(self):
		"""fhOp commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_fhOp'):
			from .Pusch_.FhOp import FhOp
			self._fhOp = FhOp(self._core, self._base)
		return self._fhOp

	@property
	def hprNumber(self):
		"""hprNumber commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hprNumber'):
			from .Pusch_.HprNumber import HprNumber
			self._hprNumber = HprNumber(self._core, self._base)
		return self._hprNumber

	@property
	def ptrs(self):
		"""ptrs commands group. 9 Sub-classes, 0 commands."""
		if not hasattr(self, '_ptrs'):
			from .Pusch_.Ptrs import Ptrs
			self._ptrs = Ptrs(self._core, self._base)
		return self._ptrs

	@property
	def resAlloc(self):
		"""resAlloc commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_resAlloc'):
			from .Pusch_.ResAlloc import ResAlloc
			self._resAlloc = ResAlloc(self._core, self._base)
		return self._resAlloc

	@property
	def txScheme(self):
		"""txScheme commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_txScheme'):
			from .Pusch_.TxScheme import TxScheme
			self._txScheme = TxScheme(self._core, self._base)
		return self._txScheme

	@property
	def typePy(self):
		"""typePy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_typePy'):
			from .Pusch_.TypePy import TypePy
			self._typePy = TypePy(self._core, self._base)
		return self._typePy

	@property
	def uci(self):
		"""uci commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_uci'):
			from .Pusch_.Uci import Uci
			self._uci = Uci(self._core, self._base)
		return self._uci
