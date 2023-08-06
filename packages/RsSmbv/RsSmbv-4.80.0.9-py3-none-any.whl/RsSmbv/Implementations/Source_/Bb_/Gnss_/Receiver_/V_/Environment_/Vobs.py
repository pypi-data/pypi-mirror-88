from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Vobs:
	"""Vobs commands group definition. 7 total commands, 5 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("vobs", core, parent)

	def clone(self) -> 'Vobs':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Vobs(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def file(self):
		"""file commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_file'):
			from .Vobs_.File import File
			self._file = File(self._core, self._base)
		return self._file

	@property
	def morientation(self):
		"""morientation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_morientation'):
			from .Vobs_.Morientation import Morientation
			self._morientation = Morientation(self._core, self._base)
		return self._morientation

	@property
	def pmodel(self):
		"""pmodel commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pmodel'):
			from .Vobs_.Pmodel import Pmodel
			self._pmodel = Pmodel(self._core, self._base)
		return self._pmodel

	@property
	def predefined(self):
		"""predefined commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_predefined'):
			from .Vobs_.Predefined import Predefined
			self._predefined = Predefined(self._core, self._base)
		return self._predefined

	@property
	def roffset(self):
		"""roffset commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_roffset'):
			from .Vobs_.Roffset import Roffset
			self._roffset = Roffset(self._core, self._base)
		return self._roffset
