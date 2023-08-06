from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Hil:
	"""Hil commands group definition. 3 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("hil", core, parent)

	def clone(self) -> 'Hil':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Hil(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def itype(self):
		"""itype commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_itype'):
			from .Hil_.Itype import Itype
			self._itype = Itype(self._core, self._base)
		return self._itype

	@property
	def port(self):
		"""port commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_port'):
			from .Hil_.Port import Port
			self._port = Port(self._core, self._base)
		return self._port

	@property
	def slatency(self):
		"""slatency commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_slatency'):
			from .Hil_.Slatency import Slatency
			self._slatency = Slatency(self._core, self._base)
		return self._slatency
