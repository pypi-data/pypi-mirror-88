from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dpdch:
	"""Dpdch commands group definition. 4 total commands, 4 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dpdch", core, parent)

	def clone(self) -> 'Dpdch':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Dpdch(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def fcio(self):
		"""fcio commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fcio'):
			from .Dpdch_.Fcio import Fcio
			self._fcio = Fcio(self._core, self._base)
		return self._fcio

	@property
	def orate(self):
		"""orate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_orate'):
			from .Dpdch_.Orate import Orate
			self._orate = Orate(self._core, self._base)
		return self._orate

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .Dpdch_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Dpdch_.State import State
			self._state = State(self._core, self._base)
		return self._state
