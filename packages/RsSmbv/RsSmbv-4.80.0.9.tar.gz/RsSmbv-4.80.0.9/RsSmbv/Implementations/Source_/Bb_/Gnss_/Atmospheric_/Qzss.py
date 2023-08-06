from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Qzss:
	"""Qzss commands group definition. 4 total commands, 1 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("qzss", core, parent)

	def clone(self) -> 'Qzss':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Qzss(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def nmessage(self):
		"""nmessage commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_nmessage'):
			from .Qzss_.Nmessage import Nmessage
			self._nmessage = Nmessage(self._core, self._base)
		return self._nmessage
