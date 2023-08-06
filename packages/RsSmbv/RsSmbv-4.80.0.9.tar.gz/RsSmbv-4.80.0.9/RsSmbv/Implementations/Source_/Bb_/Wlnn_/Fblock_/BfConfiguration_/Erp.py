from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Erp:
	"""Erp commands group definition. 3 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("erp", core, parent)

	def clone(self) -> 'Erp':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Erp(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def bpMode(self):
		"""bpMode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bpMode'):
			from .Erp_.BpMode import BpMode
			self._bpMode = BpMode(self._core, self._base)
		return self._bpMode

	@property
	def nePresent(self):
		"""nePresent commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nePresent'):
			from .Erp_.NePresent import NePresent
			self._nePresent = NePresent(self._core, self._base)
		return self._nePresent

	@property
	def uprotection(self):
		"""uprotection commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_uprotection'):
			from .Erp_.Uprotection import Uprotection
			self._uprotection = Uprotection(self._core, self._base)
		return self._uprotection
