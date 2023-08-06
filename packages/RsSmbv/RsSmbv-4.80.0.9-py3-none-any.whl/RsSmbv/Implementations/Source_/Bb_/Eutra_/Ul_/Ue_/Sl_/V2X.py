from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class V2X:
	"""V2X commands group definition. 9 total commands, 9 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("v2X", core, parent)

	def clone(self) -> 'V2X':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = V2X(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def adjc(self):
		"""adjc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_adjc'):
			from .V2X_.Adjc import Adjc
			self._adjc = Adjc(self._core, self._base)
		return self._adjc

	@property
	def bitHigh(self):
		"""bitHigh commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bitHigh'):
			from .V2X_.BitHigh import BitHigh
			self._bitHigh = BitHigh(self._core, self._base)
		return self._bitHigh

	@property
	def bitLow(self):
		"""bitLow commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bitLow'):
			from .V2X_.BitLow import BitLow
			self._bitLow = BitLow(self._core, self._base)
		return self._bitLow

	@property
	def bmpLength(self):
		"""bmpLength commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bmpLength'):
			from .V2X_.BmpLength import BmpLength
			self._bmpLength = BmpLength(self._core, self._base)
		return self._bmpLength

	@property
	def offset(self):
		"""offset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_offset'):
			from .V2X_.Offset import Offset
			self._offset = Offset(self._core, self._base)
		return self._offset

	@property
	def srbPscch(self):
		"""srbPscch commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_srbPscch'):
			from .V2X_.SrbPscch import SrbPscch
			self._srbPscch = SrbPscch(self._core, self._base)
		return self._srbPscch

	@property
	def srbSubchan(self):
		"""srbSubchan commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_srbSubchan'):
			from .V2X_.SrbSubchan import SrbSubchan
			self._srbSubchan = SrbSubchan(self._core, self._base)
		return self._srbSubchan

	@property
	def subChannels(self):
		"""subChannels commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_subChannels'):
			from .V2X_.SubChannels import SubChannels
			self._subChannels = SubChannels(self._core, self._base)
		return self._subChannels

	@property
	def subSize(self):
		"""subSize commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_subSize'):
			from .V2X_.SubSize import SubSize
			self._subSize = SubSize(self._core, self._base)
		return self._subSize
