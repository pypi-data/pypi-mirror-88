from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Niot:
	"""Niot commands group definition. 3 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("niot", core, parent)

	def clone(self) -> 'Niot':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Niot(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def rmax(self):
		"""rmax commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rmax'):
			from .Niot_.Rmax import Rmax
			self._rmax = Rmax(self._core, self._base)
		return self._rmax

	@property
	def ssOffset(self):
		"""ssOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ssOffset'):
			from .Niot_.SsOffset import SsOffset
			self._ssOffset = SsOffset(self._core, self._base)
		return self._ssOffset

	@property
	def stsFrame(self):
		"""stsFrame commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_stsFrame'):
			from .Niot_.StsFrame import StsFrame
			self._stsFrame = StsFrame(self._core, self._base)
		return self._stsFrame
