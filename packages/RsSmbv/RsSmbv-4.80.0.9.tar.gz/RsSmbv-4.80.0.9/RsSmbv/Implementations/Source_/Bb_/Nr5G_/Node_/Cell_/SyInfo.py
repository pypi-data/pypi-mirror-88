from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SyInfo:
	"""SyInfo commands group definition. 3 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("syInfo", core, parent)

	def clone(self) -> 'SyInfo':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SyInfo(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def hacbook(self):
		"""hacbook commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hacbook'):
			from .SyInfo_.Hacbook import Hacbook
			self._hacbook = Hacbook(self._core, self._base)
		return self._hacbook

	@property
	def sfOffset(self):
		"""sfOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sfOffset'):
			from .SyInfo_.SfOffset import SfOffset
			self._sfOffset = SfOffset(self._core, self._base)
		return self._sfOffset

	@property
	def sul(self):
		"""sul commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_sul'):
			from .SyInfo_.Sul import Sul
			self._sul = Sul(self._core, self._base)
		return self._sul
