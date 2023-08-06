from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rnti:
	"""Rnti commands group definition. 7 total commands, 7 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rnti", core, parent)

	def clone(self) -> 'Rnti':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Rnti(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def airnti(self):
		"""airnti commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_airnti'):
			from .Rnti_.Airnti import Airnti
			self._airnti = Airnti(self._core, self._base)
		return self._airnti

	@property
	def cirnti(self):
		"""cirnti commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cirnti'):
			from .Rnti_.Cirnti import Cirnti
			self._cirnti = Cirnti(self._core, self._base)
		return self._cirnti

	@property
	def int(self):
		"""int commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_int'):
			from .Rnti_.Int import Int
			self._int = Int(self._core, self._base)
		return self._int

	@property
	def psrnti(self):
		"""psrnti commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_psrnti'):
			from .Rnti_.Psrnti import Psrnti
			self._psrnti = Psrnti(self._core, self._base)
		return self._psrnti

	@property
	def pucch(self):
		"""pucch commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pucch'):
			from .Rnti_.Pucch import Pucch
			self._pucch = Pucch(self._core, self._base)
		return self._pucch

	@property
	def pusch(self):
		"""pusch commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pusch'):
			from .Rnti_.Pusch import Pusch
			self._pusch = Pusch(self._core, self._base)
		return self._pusch

	@property
	def srs(self):
		"""srs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_srs'):
			from .Rnti_.Srs import Srs
			self._srs = Srs(self._core, self._base)
		return self._srs
