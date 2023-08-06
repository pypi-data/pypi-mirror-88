from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Iq:
	"""Iq commands group definition. 23 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("iq", core, parent)

	def clone(self) -> 'Iq':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Iq(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def optimization(self):
		"""optimization commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_optimization'):
			from .Iq_.Optimization import Optimization
			self._optimization = Optimization(self._core, self._base)
		return self._optimization

	@property
	def user(self):
		"""user commands group. 4 Sub-classes, 4 commands."""
		if not hasattr(self, '_user'):
			from .Iq_.User import User
			self._user = User(self._core, self._base)
		return self._user
