from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Fresponse:
	"""Fresponse commands group definition. 49 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("fresponse", core, parent)

	def clone(self) -> 'Fresponse':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Fresponse(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def iq(self):
		"""iq commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_iq'):
			from .Fresponse_.Iq import Iq
			self._iq = Iq(self._core, self._base)
		return self._iq

	@property
	def rf(self):
		"""rf commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_rf'):
			from .Fresponse_.Rf import Rf
			self._rf = Rf(self._core, self._base)
		return self._rf
