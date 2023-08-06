from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Template:
	"""Template commands group definition. 5 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("template", core, parent)

	def clone(self) -> 'Template':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Template(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def predefined(self):
		"""predefined commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_predefined'):
			from .Template_.Predefined import Predefined
			self._predefined = Predefined(self._core, self._base)
		return self._predefined

	@property
	def user(self):
		"""user commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_user'):
			from .Template_.User import User
			self._user = User(self._core, self._base)
		return self._user
