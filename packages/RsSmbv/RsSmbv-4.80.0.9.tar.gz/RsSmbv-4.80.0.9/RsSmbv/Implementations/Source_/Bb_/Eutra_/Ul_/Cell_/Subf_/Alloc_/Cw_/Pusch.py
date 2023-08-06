from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pusch:
	"""Pusch commands group definition. 7 total commands, 6 Sub-groups, 0 group commands"""

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
	def ccoding(self):
		"""ccoding commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_ccoding'):
			from .Pusch_.Ccoding import Ccoding
			self._ccoding = Ccoding(self._core, self._base)
		return self._ccoding

	@property
	def harq(self):
		"""harq commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_harq'):
			from .Pusch_.Harq import Harq
			self._harq = Harq(self._core, self._base)
		return self._harq

	@property
	def physBits(self):
		"""physBits commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_physBits'):
			from .Pusch_.PhysBits import PhysBits
			self._physBits = PhysBits(self._core, self._base)
		return self._physBits

	@property
	def ri(self):
		"""ri commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ri'):
			from .Pusch_.Ri import Ri
			self._ri = Ri(self._core, self._base)
		return self._ri

	@property
	def ulsch(self):
		"""ulsch commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ulsch'):
			from .Pusch_.Ulsch import Ulsch
			self._ulsch = Ulsch(self._core, self._base)
		return self._ulsch

	@property
	def modulation(self):
		"""modulation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_modulation'):
			from .Pusch_.Modulation import Modulation
			self._modulation = Modulation(self._core, self._base)
		return self._modulation
