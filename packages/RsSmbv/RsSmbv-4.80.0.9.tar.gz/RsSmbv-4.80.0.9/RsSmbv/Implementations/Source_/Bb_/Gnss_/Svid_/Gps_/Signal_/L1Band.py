from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class L1Band:
	"""L1Band commands group definition. 40 total commands, 5 Sub-groups, 0 group commands"""

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
	def c1C(self):
		"""c1C commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_c1C'):
			from .L1Band_.C1C import C1C
			self._c1C = C1C(self._core, self._base)
		return self._c1C

	@property
	def c2C(self):
		"""c2C commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_c2C'):
			from .L1Band_.C2C import C2C
			self._c2C = C2C(self._core, self._base)
		return self._c2C

	@property
	def ca(self):
		"""ca commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_ca'):
			from .L1Band_.Ca import Ca
			self._ca = Ca(self._core, self._base)
		return self._ca

	@property
	def l1C(self):
		"""l1C commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_l1C'):
			from .L1Band_.L1C import L1C
			self._l1C = L1C(self._core, self._base)
		return self._l1C

	@property
	def p(self):
		"""p commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_p'):
			from .L1Band_.P import P
			self._p = P(self._core, self._base)
		return self._p
