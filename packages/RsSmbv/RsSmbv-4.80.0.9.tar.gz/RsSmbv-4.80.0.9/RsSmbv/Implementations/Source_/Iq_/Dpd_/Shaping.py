from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Shaping:
	"""Shaping commands group definition. 19 total commands, 4 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("shaping", core, parent)

	def clone(self) -> 'Shaping':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Shaping(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def mode(self):
		"""mode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mode'):
			from .Shaping_.Mode import Mode
			self._mode = Mode(self._core, self._base)
		return self._mode

	@property
	def normalized(self):
		"""normalized commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_normalized'):
			from .Shaping_.Normalized import Normalized
			self._normalized = Normalized(self._core, self._base)
		return self._normalized

	@property
	def polynomial(self):
		"""polynomial commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_polynomial'):
			from .Shaping_.Polynomial import Polynomial
			self._polynomial = Polynomial(self._core, self._base)
		return self._polynomial

	@property
	def table(self):
		"""table commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_table'):
			from .Shaping_.Table import Table
			self._table = Table(self._core, self._base)
		return self._table
