from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class L1Band:
	"""L1Band commands group definition. 2 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("l1Band", core, parent)

	def clone(self) -> 'L1Band':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = L1Band(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def ca(self):
		"""ca commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ca'):
			from .L1Band_.Ca import Ca
			self._ca = Ca(self._core, self._base)
		return self._ca

	@property
	def p(self):
		"""p commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_p'):
			from .L1Band_.P import P
			self._p = P(self._core, self._base)
		return self._p
