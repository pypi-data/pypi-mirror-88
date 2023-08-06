from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mtsphy:
	"""Mtsphy commands group definition. 3 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mtsphy", core, parent)

	def clone(self) -> 'Mtsphy':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Mtsphy(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def l1M(self):
		"""l1M commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_l1M'):
			from .Mtsphy_.L1M import L1M
			self._l1M = L1M(self._core, self._base)
		return self._l1M

	@property
	def l2M(self):
		"""l2M commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_l2M'):
			from .Mtsphy_.L2M import L2M
			self._l2M = L2M(self._core, self._base)
		return self._l2M

	@property
	def lcod(self):
		"""lcod commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_lcod'):
			from .Mtsphy_.Lcod import Lcod
			self._lcod = Lcod(self._core, self._base)
		return self._lcod
