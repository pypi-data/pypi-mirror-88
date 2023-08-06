from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Category:
	"""Category commands group definition. 46 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("category", core, parent)

	def clone(self) -> 'Category':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Category(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def satellite(self):
		"""satellite commands group. 20 Sub-classes, 1 commands."""
		if not hasattr(self, '_satellite'):
			from .Category_.Satellite import Satellite
			self._satellite = Satellite(self._core, self._base)
		return self._satellite

	@property
	def umotion(self):
		"""umotion commands group. 3 Sub-classes, 1 commands."""
		if not hasattr(self, '_umotion'):
			from .Category_.Umotion import Umotion
			self._umotion = Umotion(self._core, self._base)
		return self._umotion
