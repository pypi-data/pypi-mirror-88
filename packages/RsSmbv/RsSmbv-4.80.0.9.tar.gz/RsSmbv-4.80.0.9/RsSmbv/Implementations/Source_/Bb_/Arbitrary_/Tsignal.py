from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tsignal:
	"""Tsignal commands group definition. 16 total commands, 4 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tsignal", core, parent)

	def clone(self) -> 'Tsignal':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Tsignal(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def awgn(self):
		"""awgn commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_awgn'):
			from .Tsignal_.Awgn import Awgn
			self._awgn = Awgn(self._core, self._base)
		return self._awgn

	@property
	def ciq(self):
		"""ciq commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_ciq'):
			from .Tsignal_.Ciq import Ciq
			self._ciq = Ciq(self._core, self._base)
		return self._ciq

	@property
	def rectangle(self):
		"""rectangle commands group. 1 Sub-classes, 4 commands."""
		if not hasattr(self, '_rectangle'):
			from .Tsignal_.Rectangle import Rectangle
			self._rectangle = Rectangle(self._core, self._base)
		return self._rectangle

	@property
	def sine(self):
		"""sine commands group. 1 Sub-classes, 3 commands."""
		if not hasattr(self, '_sine'):
			from .Tsignal_.Sine import Sine
			self._sine = Sine(self._core, self._base)
		return self._sine
