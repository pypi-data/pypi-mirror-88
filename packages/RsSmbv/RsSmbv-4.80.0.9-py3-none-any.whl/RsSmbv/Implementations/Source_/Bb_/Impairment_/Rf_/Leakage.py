from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Leakage:
	"""Leakage commands group definition. 2 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("leakage", core, parent)

	def clone(self) -> 'Leakage':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Leakage(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def icomponent(self):
		"""icomponent commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_icomponent'):
			from .Leakage_.Icomponent import Icomponent
			self._icomponent = Icomponent(self._core, self._base)
		return self._icomponent

	@property
	def qcomponent(self):
		"""qcomponent commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_qcomponent'):
			from .Leakage_.Qcomponent import Qcomponent
			self._qcomponent = Qcomponent(self._core, self._base)
		return self._qcomponent
