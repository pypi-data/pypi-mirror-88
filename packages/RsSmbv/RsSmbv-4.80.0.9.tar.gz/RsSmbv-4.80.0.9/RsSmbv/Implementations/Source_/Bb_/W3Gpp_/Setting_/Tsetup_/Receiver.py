from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Receiver:
	"""Receiver commands group definition. 4 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("receiver", core, parent)

	def clone(self) -> 'Receiver':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Receiver(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def bstation(self):
		"""bstation commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_bstation'):
			from .Receiver_.Bstation import Bstation
			self._bstation = Bstation(self._core, self._base)
		return self._bstation

	@property
	def mstation(self):
		"""mstation commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_mstation'):
			from .Receiver_.Mstation import Mstation
			self._mstation = Mstation(self._core, self._base)
		return self._mstation
