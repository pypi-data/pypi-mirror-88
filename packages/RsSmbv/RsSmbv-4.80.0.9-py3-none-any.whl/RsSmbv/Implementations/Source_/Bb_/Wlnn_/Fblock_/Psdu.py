from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Psdu:
	"""Psdu commands group definition. 3 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("psdu", core, parent)

	def clone(self) -> 'Psdu':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Psdu(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def brate(self):
		"""brate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_brate'):
			from .Psdu_.Brate import Brate
			self._brate = Brate(self._core, self._base)
		return self._brate

	@property
	def bspreading(self):
		"""bspreading commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_bspreading'):
			from .Psdu_.Bspreading import Bspreading
			self._bspreading = Bspreading(self._core, self._base)
		return self._bspreading

	@property
	def modulation(self):
		"""modulation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_modulation'):
			from .Psdu_.Modulation import Modulation
			self._modulation = Modulation(self._core, self._base)
		return self._modulation
