from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.RepeatedCapability import RepeatedCapability
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Channel:
	"""Channel commands group definition. 10 total commands, 7 Sub-groups, 0 group commands
	Repeated Capability: Channel, default value after init: Channel.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("channel", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_channel_get', 'repcap_channel_set', repcap.Channel.Nr1)

	def clone(self) -> 'Channel':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Channel(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	def repcap_channel_set(self, enum_value: repcap.Channel) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Channel.Default
		Default value after init: Channel.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_channel_get(self) -> repcap.Channel:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def data(self):
		"""data commands group. 3 Sub-classes, 1 commands."""
		if not hasattr(self, '_data'):
			from .Channel_.Data import Data
			self._data = Data(self._core, self._base)
		return self._data

	@property
	def flength(self):
		"""flength commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_flength'):
			from .Channel_.Flength import Flength
			self._flength = Flength(self._core, self._base)
		return self._flength

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .Channel_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power

	@property
	def spreading(self):
		"""spreading commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_spreading'):
			from .Channel_.Spreading import Spreading
			self._spreading = Spreading(self._core, self._base)
		return self._spreading

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Channel_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def typePy(self):
		"""typePy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_typePy'):
			from .Channel_.TypePy import TypePy
			self._typePy = TypePy(self._core, self._base)
		return self._typePy

	@property
	def wcode(self):
		"""wcode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_wcode'):
			from .Channel_.Wcode import Wcode
			self._wcode = Wcode(self._core, self._base)
		return self._wcode
