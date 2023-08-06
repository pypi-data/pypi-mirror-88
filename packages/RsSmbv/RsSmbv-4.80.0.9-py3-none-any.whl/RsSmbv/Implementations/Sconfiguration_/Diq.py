from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Diq:
	"""Diq commands group definition. 2 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("diq", core, parent)

	def clone(self) -> 'Diq':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Diq(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def bbmm1(self):
		"""bbmm1 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bbmm1'):
			from .Diq_.Bbmm1 import Bbmm1
			self._bbmm1 = Bbmm1(self._core, self._base)
		return self._bbmm1

	@property
	def bbmm2(self):
		"""bbmm2 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bbmm2'):
			from .Diq_.Bbmm2 import Bbmm2
			self._bbmm2 = Bbmm2(self._core, self._base)
		return self._bbmm2
