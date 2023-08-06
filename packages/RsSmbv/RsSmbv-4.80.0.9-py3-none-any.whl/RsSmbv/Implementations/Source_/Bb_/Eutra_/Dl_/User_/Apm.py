from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Apm:
	"""Apm commands group definition. 7 total commands, 6 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("apm", core, parent)

	def clone(self) -> 'Apm':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Apm(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def cbci(self):
		"""cbci commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cbci'):
			from .Apm_.Cbci import Cbci
			self._cbci = Cbci(self._core, self._base)
		return self._cbci

	@property
	def cbIndex(self):
		"""cbIndex commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cbIndex'):
			from .Apm_.CbIndex import CbIndex
			self._cbIndex = CbIndex(self._core, self._base)
		return self._cbIndex

	@property
	def cbua(self):
		"""cbua commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cbua'):
			from .Apm_.Cbua import Cbua
			self._cbua = Cbua(self._core, self._base)
		return self._cbua

	@property
	def mapCoordinates(self):
		"""mapCoordinates commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mapCoordinates'):
			from .Apm_.MapCoordinates import MapCoordinates
			self._mapCoordinates = MapCoordinates(self._core, self._base)
		return self._mapCoordinates

	@property
	def mode(self):
		"""mode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mode'):
			from .Apm_.Mode import Mode
			self._mode = Mode(self._core, self._base)
		return self._mode

	@property
	def layer(self):
		"""layer commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_layer'):
			from .Apm_.Layer import Layer
			self._layer = Layer(self._core, self._base)
		return self._layer
