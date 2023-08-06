from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Polynomial:
	"""Polynomial commands group definition. 4 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("polynomial", core, parent)

	def clone(self) -> 'Polynomial':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Polynomial(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def coefficients(self):
		"""coefficients commands group. 2 Sub-classes, 2 commands."""
		if not hasattr(self, '_coefficients'):
			from .Polynomial_.Coefficients import Coefficients
			self._coefficients = Coefficients(self._core, self._base)
		return self._coefficients
