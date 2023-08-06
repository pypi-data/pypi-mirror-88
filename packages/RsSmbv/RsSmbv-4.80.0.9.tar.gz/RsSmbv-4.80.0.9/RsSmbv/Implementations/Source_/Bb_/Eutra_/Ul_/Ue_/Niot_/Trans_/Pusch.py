from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pusch:
	"""Pusch commands group definition. 8 total commands, 8 Sub-groups, 0 group commands"""

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
	def esupport(self):
		"""esupport commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_esupport'):
			from .Pusch_.Esupport import Esupport
			self._esupport = Esupport(self._core, self._base)
		return self._esupport

	@property
	def etbs(self):
		"""etbs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_etbs'):
			from .Pusch_.Etbs import Etbs
			self._etbs = Etbs(self._core, self._base)
		return self._etbs

	@property
	def etrSize(self):
		"""etrSize commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_etrSize'):
			from .Pusch_.EtrSize import EtrSize
			self._etrSize = EtrSize(self._core, self._base)
		return self._etrSize

	@property
	def physBits(self):
		"""physBits commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_physBits'):
			from .Pusch_.PhysBits import PhysBits
			self._physBits = PhysBits(self._core, self._base)
		return self._physBits

	@property
	def ruIndex(self):
		"""ruIndex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ruIndex'):
			from .Pusch_.RuIndex import RuIndex
			self._ruIndex = RuIndex(self._core, self._base)
		return self._ruIndex

	@property
	def rvIndex(self):
		"""rvIndex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rvIndex'):
			from .Pusch_.RvIndex import RvIndex
			self._rvIndex = RvIndex(self._core, self._base)
		return self._rvIndex

	@property
	def tbIndex(self):
		"""tbIndex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tbIndex'):
			from .Pusch_.TbIndex import TbIndex
			self._tbIndex = TbIndex(self._core, self._base)
		return self._tbIndex

	@property
	def tbSize(self):
		"""tbSize commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tbSize'):
			from .Pusch_.TbSize import TbSize
			self._tbSize = TbSize(self._core, self._base)
		return self._tbSize
