from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Uci:
	"""Uci commands group definition. 6 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("uci", core, parent)

	def clone(self) -> 'Uci':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Uci(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def ack(self):
		"""ack commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_ack'):
			from .Uci_.Ack import Ack
			self._ack = Ack(self._core, self._base)
		return self._ack

	@property
	def csi1(self):
		"""csi1 commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_csi1'):
			from .Uci_.Csi1 import Csi1
			self._csi1 = Csi1(self._core, self._base)
		return self._csi1

	@property
	def csi2(self):
		"""csi2 commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_csi2'):
			from .Uci_.Csi2 import Csi2
			self._csi2 = Csi2(self._core, self._base)
		return self._csi2
