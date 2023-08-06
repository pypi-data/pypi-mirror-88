from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Npdcch:
	"""Npdcch commands group definition. 3 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("npdcch", core, parent)

	def clone(self) -> 'Npdcch':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Npdcch(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def fmt(self):
		"""fmt commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fmt'):
			from .Npdcch_.Fmt import Fmt
			self._fmt = Fmt(self._core, self._base)
		return self._fmt

	@property
	def oind(self):
		"""oind commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_oind'):
			from .Npdcch_.Oind import Oind
			self._oind = Oind(self._core, self._base)
		return self._oind

	@property
	def rep(self):
		"""rep commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rep'):
			from .Npdcch_.Rep import Rep
			self._rep = Rep(self._core, self._base)
		return self._rep
