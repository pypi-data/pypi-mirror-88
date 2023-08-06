from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TxScheme:
	"""TxScheme commands group definition. 3 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("txScheme", core, parent)

	def clone(self) -> 'TxScheme':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = TxScheme(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def cdmData(self):
		"""cdmData commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cdmData'):
			from .TxScheme_.CdmData import CdmData
			self._cdmData = CdmData(self._core, self._base)
		return self._cdmData

	@property
	def intervp(self):
		"""intervp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_intervp'):
			from .TxScheme_.Intervp import Intervp
			self._intervp = Intervp(self._core, self._base)
		return self._intervp

	@property
	def nlayers(self):
		"""nlayers commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nlayers'):
			from .TxScheme_.Nlayers import Nlayers
			self._nlayers = Nlayers(self._core, self._base)
		return self._nlayers
