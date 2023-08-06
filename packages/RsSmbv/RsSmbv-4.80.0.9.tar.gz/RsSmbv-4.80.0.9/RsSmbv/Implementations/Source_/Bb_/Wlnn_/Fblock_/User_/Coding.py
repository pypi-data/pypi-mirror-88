from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Coding:
	"""Coding commands group definition. 3 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("coding", core, parent)

	def clone(self) -> 'Coding':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Coding(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def encoder(self):
		"""encoder commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_encoder'):
			from .Coding_.Encoder import Encoder
			self._encoder = Encoder(self._core, self._base)
		return self._encoder

	@property
	def rate(self):
		"""rate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rate'):
			from .Coding_.Rate import Rate
			self._rate = Rate(self._core, self._base)
		return self._rate

	@property
	def typePy(self):
		"""typePy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_typePy'):
			from .Coding_.TypePy import TypePy
			self._typePy = TypePy(self._core, self._base)
		return self._typePy
