from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.RepeatedCapability import RepeatedCapability
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class A:
	"""A commands group definition. 9 total commands, 9 Sub-groups, 0 group commands
	Repeated Capability: Channel, default value after init: Channel.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("a", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_channel_get', 'repcap_channel_set', repcap.Channel.Nr1)

	def clone(self) -> 'A':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = A(self._core, self._base.parent)
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
	def apattern(self):
		"""apattern commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_apattern'):
			from .A_.Apattern import Apattern
			self._apattern = Apattern(self._core, self._base)
		return self._apattern

	@property
	def body(self):
		"""body commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_body'):
			from .A_.Body import Body
			self._body = Body(self._core, self._base)
		return self._body

	@property
	def dbank(self):
		"""dbank commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dbank'):
			from .A_.Dbank import Dbank
			self._dbank = Dbank(self._core, self._base)
		return self._dbank

	@property
	def delevation(self):
		"""delevation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_delevation'):
			from .A_.Delevation import Delevation
			self._delevation = Delevation(self._core, self._base)
		return self._delevation

	@property
	def dheading(self):
		"""dheading commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dheading'):
			from .A_.Dheading import Dheading
			self._dheading = Dheading(self._core, self._base)
		return self._dheading

	@property
	def dx(self):
		"""dx commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dx'):
			from .A_.Dx import Dx
			self._dx = Dx(self._core, self._base)
		return self._dx

	@property
	def dy(self):
		"""dy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dy'):
			from .A_.Dy import Dy
			self._dy = Dy(self._core, self._base)
		return self._dy

	@property
	def dz(self):
		"""dz commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dz'):
			from .A_.Dz import Dz
			self._dz = Dz(self._core, self._base)
		return self._dz

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .A_.State import State
			self._state = State(self._core, self._base)
		return self._state
