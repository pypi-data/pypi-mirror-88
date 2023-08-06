from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Econfig:
	"""Econfig commands group definition. 2 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("econfig", core, parent)

	def clone(self) -> 'Econfig':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Econfig(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def pconfig(self):
		"""pconfig commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_pconfig'):
			from .Econfig_.Pconfig import Pconfig
			self._pconfig = Pconfig(self._core, self._base)
		return self._pconfig
