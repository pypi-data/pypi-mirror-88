from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pusch:
	"""Pusch commands group definition. 4 total commands, 4 Sub-groups, 0 group commands"""

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
	def bd22(self):
		"""bd22 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bd22'):
			from .Pusch_.Bd22 import Bd22
			self._bd22 = Bd22(self._core, self._base)
		return self._bd22

	@property
	def oi01(self):
		"""oi01 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_oi01'):
			from .Pusch_.Oi01 import Oi01
			self._oi01 = Oi01(self._core, self._base)
		return self._oi01

	@property
	def oi11(self):
		"""oi11 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_oi11'):
			from .Pusch_.Oi11 import Oi11
			self._oi11 = Oi11(self._core, self._base)
		return self._oi11

	@property
	def tpas(self):
		"""tpas commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tpas'):
			from .Pusch_.Tpas import Tpas
			self._tpas = Tpas(self._core, self._base)
		return self._tpas
