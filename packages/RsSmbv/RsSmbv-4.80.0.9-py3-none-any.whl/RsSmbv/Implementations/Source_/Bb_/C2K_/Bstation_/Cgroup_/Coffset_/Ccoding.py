from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ccoding:
	"""Ccoding commands group definition. 8 total commands, 8 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ccoding", core, parent)

	def clone(self) -> 'Ccoding':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Ccoding(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def binterleaver(self):
		"""binterleaver commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_binterleaver'):
			from .Ccoding_.Binterleaver import Binterleaver
			self._binterleaver = Binterleaver(self._core, self._base)
		return self._binterleaver

	@property
	def bitFrame(self):
		"""bitFrame commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bitFrame'):
			from .Ccoding_.BitFrame import BitFrame
			self._bitFrame = BitFrame(self._core, self._base)
		return self._bitFrame

	@property
	def crc(self):
		"""crc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_crc'):
			from .Ccoding_.Crc import Crc
			self._crc = Crc(self._core, self._base)
		return self._crc

	@property
	def data(self):
		"""data commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_data'):
			from .Ccoding_.Data import Data
			self._data = Data(self._core, self._base)
		return self._data

	@property
	def mode(self):
		"""mode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mode'):
			from .Ccoding_.Mode import Mode
			self._mode = Mode(self._core, self._base)
		return self._mode

	@property
	def spuncture(self):
		"""spuncture commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_spuncture'):
			from .Ccoding_.Spuncture import Spuncture
			self._spuncture = Spuncture(self._core, self._base)
		return self._spuncture

	@property
	def srepetition(self):
		"""srepetition commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_srepetition'):
			from .Ccoding_.Srepetition import Srepetition
			self._srepetition = Srepetition(self._core, self._base)
		return self._srepetition

	@property
	def typePy(self):
		"""typePy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_typePy'):
			from .Ccoding_.TypePy import TypePy
			self._typePy = TypePy(self._core, self._base)
		return self._typePy
