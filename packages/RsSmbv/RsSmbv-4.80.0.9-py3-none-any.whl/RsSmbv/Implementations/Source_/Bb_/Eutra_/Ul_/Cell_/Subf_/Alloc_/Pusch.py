from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pusch:
	"""Pusch commands group definition. 26 total commands, 12 Sub-groups, 0 group commands"""

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
	def codewords(self):
		"""codewords commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_codewords'):
			from .Pusch_.Codewords import Codewords
			self._codewords = Codewords(self._core, self._base)
		return self._codewords

	@property
	def conflict(self):
		"""conflict commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_conflict'):
			from .Pusch_.Conflict import Conflict
			self._conflict = Conflict(self._core, self._base)
		return self._conflict

	@property
	def cqi(self):
		"""cqi commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_cqi'):
			from .Pusch_.Cqi import Cqi
			self._cqi = Cqi(self._core, self._base)
		return self._cqi

	@property
	def drs(self):
		"""drs commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_drs'):
			from .Pusch_.Drs import Drs
			self._drs = Drs(self._core, self._base)
		return self._drs

	@property
	def fhOp(self):
		"""fhOp commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_fhOp'):
			from .Pusch_.FhOp import FhOp
			self._fhOp = FhOp(self._core, self._base)
		return self._fhOp

	@property
	def harq(self):
		"""harq commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_harq'):
			from .Pusch_.Harq import Harq
			self._harq = Harq(self._core, self._base)
		return self._harq

	@property
	def mapping(self):
		"""mapping commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mapping'):
			from .Pusch_.Mapping import Mapping
			self._mapping = Mapping(self._core, self._base)
		return self._mapping

	@property
	def ndmrs(self):
		"""ndmrs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ndmrs'):
			from .Pusch_.Ndmrs import Ndmrs
			self._ndmrs = Ndmrs(self._core, self._base)
		return self._ndmrs

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .Pusch_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power

	@property
	def precoding(self):
		"""precoding commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_precoding'):
			from .Pusch_.Precoding import Precoding
			self._precoding = Precoding(self._core, self._base)
		return self._precoding

	@property
	def ri(self):
		"""ri commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_ri'):
			from .Pusch_.Ri import Ri
			self._ri = Ri(self._core, self._base)
		return self._ri

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Pusch_.State import State
			self._state = State(self._core, self._base)
		return self._state
