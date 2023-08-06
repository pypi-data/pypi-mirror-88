from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dch:
	"""Dch commands group definition. 88 total commands, 17 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dch", core, parent)

	def clone(self) -> 'Dch':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Dch(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def bit(self):
		"""bit commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_bit'):
			from .Dch_.Bit import Bit
			self._bit = Bit(self._core, self._base)
		return self._bit

	@property
	def block(self):
		"""block commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_block'):
			from .Dch_.Block import Block
			self._block = Block(self._core, self._base)
		return self._block

	@property
	def bpFrame(self):
		"""bpFrame commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bpFrame'):
			from .Dch_.BpFrame import BpFrame
			self._bpFrame = BpFrame(self._core, self._base)
		return self._bpFrame

	@property
	def ccount(self):
		"""ccount commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ccount'):
			from .Dch_.Ccount import Ccount
			self._ccount = Ccount(self._core, self._base)
		return self._ccount

	@property
	def dcch(self):
		"""dcch commands group. 10 Sub-classes, 0 commands."""
		if not hasattr(self, '_dcch'):
			from .Dch_.Dcch import Dcch
			self._dcch = Dcch(self._core, self._base)
		return self._dcch

	@property
	def dtch(self):
		"""dtch commands group. 10 Sub-classes, 0 commands."""
		if not hasattr(self, '_dtch'):
			from .Dch_.Dtch import Dtch
			self._dtch = Dtch(self._core, self._base)
		return self._dtch

	@property
	def hsch(self):
		"""hsch commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_hsch'):
			from .Dch_.Hsch import Hsch
			self._hsch = Hsch(self._core, self._base)
		return self._hsch

	@property
	def hsdpa(self):
		"""hsdpa commands group. 15 Sub-classes, 0 commands."""
		if not hasattr(self, '_hsdpa'):
			from .Dch_.Hsdpa import Hsdpa
			self._hsdpa = Hsdpa(self._core, self._base)
		return self._hsdpa

	@property
	def hsich(self):
		"""hsich commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_hsich'):
			from .Dch_.Hsich import Hsich
			self._hsich = Hsich(self._core, self._base)
		return self._hsich

	@property
	def hsupa(self):
		"""hsupa commands group. 20 Sub-classes, 0 commands."""
		if not hasattr(self, '_hsupa'):
			from .Dch_.Hsupa import Hsupa
			self._hsupa = Hsupa(self._core, self._base)
		return self._hsupa

	@property
	def rupLayer(self):
		"""rupLayer commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rupLayer'):
			from .Dch_.RupLayer import RupLayer
			self._rupLayer = RupLayer(self._core, self._base)
		return self._rupLayer

	@property
	def scsMode(self):
		"""scsMode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scsMode'):
			from .Dch_.ScsMode import ScsMode
			self._scsMode = ScsMode(self._core, self._base)
		return self._scsMode

	@property
	def sformat(self):
		"""sformat commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sformat'):
			from .Dch_.Sformat import Sformat
			self._sformat = Sformat(self._core, self._base)
		return self._sformat

	@property
	def slotState(self):
		"""slotState commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_slotState'):
			from .Dch_.SlotState import SlotState
			self._slotState = SlotState(self._core, self._base)
		return self._slotState

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Dch_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def tsCount(self):
		"""tsCount commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tsCount'):
			from .Dch_.TsCount import TsCount
			self._tsCount = TsCount(self._core, self._base)
		return self._tsCount

	@property
	def typePy(self):
		"""typePy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_typePy'):
			from .Dch_.TypePy import TypePy
			self._typePy = TypePy(self._core, self._base)
		return self._typePy
