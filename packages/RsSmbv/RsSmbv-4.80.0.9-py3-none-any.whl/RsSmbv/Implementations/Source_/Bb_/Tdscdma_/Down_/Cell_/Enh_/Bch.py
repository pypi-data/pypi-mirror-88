from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Bch:
	"""Bch commands group definition. 18 total commands, 7 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("bch", core, parent)

	def clone(self) -> 'Bch':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Bch(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def bpFrame(self):
		"""bpFrame commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bpFrame'):
			from .Bch_.BpFrame import BpFrame
			self._bpFrame = BpFrame(self._core, self._base)
		return self._bpFrame

	@property
	def dtch(self):
		"""dtch commands group. 10 Sub-classes, 0 commands."""
		if not hasattr(self, '_dtch'):
			from .Bch_.Dtch import Dtch
			self._dtch = Dtch(self._core, self._base)
		return self._dtch

	@property
	def scsMode(self):
		"""scsMode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scsMode'):
			from .Bch_.ScsMode import ScsMode
			self._scsMode = ScsMode(self._core, self._base)
		return self._scsMode

	@property
	def sformat(self):
		"""sformat commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sformat'):
			from .Bch_.Sformat import Sformat
			self._sformat = Sformat(self._core, self._base)
		return self._sformat

	@property
	def slotState(self):
		"""slotState commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_slotState'):
			from .Bch_.SlotState import SlotState
			self._slotState = SlotState(self._core, self._base)
		return self._slotState

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Bch_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def typePy(self):
		"""typePy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_typePy'):
			from .Bch_.TypePy import TypePy
			self._typePy = TypePy(self._core, self._base)
		return self._typePy
