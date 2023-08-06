from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.RepeatedCapability import RepeatedCapability
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Frame:
	"""Frame commands group definition. 37 total commands, 5 Sub-groups, 0 group commands
	Repeated Capability: FrameIx, default value after init: FrameIx.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("frame", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_frameIx_get', 'repcap_frameIx_set', repcap.FrameIx.Nr1)

	def clone(self) -> 'Frame':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Frame(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	def repcap_frameIx_set(self, enum_value: repcap.FrameIx) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to FrameIx.Default
		Default value after init: FrameIx.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_frameIx_get(self) -> repcap.FrameIx:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def repetitions(self):
		"""repetitions commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_repetitions'):
			from .Frame_.Repetitions import Repetitions
			self._repetitions = Repetitions(self._core, self._base)
		return self._repetitions

	@property
	def ulist(self):
		"""ulist commands group. 2 Sub-classes, 2 commands."""
		if not hasattr(self, '_ulist'):
			from .Frame_.Ulist import Ulist
			self._ulist = Ulist(self._core, self._base)
		return self._ulist

	@property
	def multiSlot(self):
		"""multiSlot commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_multiSlot'):
			from .Frame_.MultiSlot import MultiSlot
			self._multiSlot = MultiSlot(self._core, self._base)
		return self._multiSlot

	@property
	def predefined(self):
		"""predefined commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_predefined'):
			from .Frame_.Predefined import Predefined
			self._predefined = Predefined(self._core, self._base)
		return self._predefined

	@property
	def slot(self):
		"""slot commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_slot'):
			from .Frame_.Slot import Slot
			self._slot = Slot(self._core, self._base)
		return self._slot
