from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rpc:
	"""Rpc commands group definition. 5 total commands, 4 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rpc", core, parent)

	def clone(self) -> 'Rpc':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Rpc(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def inject(self):
		"""inject commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_inject'):
			from .Rpc_.Inject import Inject
			self._inject = Inject(self._core, self._base)
		return self._inject

	@property
	def mode(self):
		"""mode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mode'):
			from .Rpc_.Mode import Mode
			self._mode = Mode(self._core, self._base)
		return self._mode

	@property
	def range(self):
		"""range commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_range'):
			from .Rpc_.Range import Range
			self._range = Range(self._core, self._base)
		return self._range

	@property
	def zone(self):
		"""zone commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_zone'):
			from .Rpc_.Zone import Zone
			self._zone = Zone(self._core, self._base)
		return self._zone
