from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.RepeatedCapability import RepeatedCapability
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rf:
	"""Rf commands group definition. 8 total commands, 7 Sub-groups, 0 group commands
	Repeated Capability: Channel, default value after init: Channel.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rf", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_channel_get', 'repcap_channel_set', repcap.Channel.Nr1)

	def clone(self) -> 'Rf':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Rf(self._core, self._base.parent)
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
	def delay(self):
		"""delay commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_delay'):
			from .Rf_.Delay import Delay
			self._delay = Delay(self._core, self._base)
		return self._delay

	@property
	def iqRatio(self):
		"""iqRatio commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_iqRatio'):
			from .Rf_.IqRatio import IqRatio
			self._iqRatio = IqRatio(self._core, self._base)
		return self._iqRatio

	@property
	def leakage(self):
		"""leakage commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_leakage'):
			from .Rf_.Leakage import Leakage
			self._leakage = Leakage(self._core, self._base)
		return self._leakage

	@property
	def poffset(self):
		"""poffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_poffset'):
			from .Rf_.Poffset import Poffset
			self._poffset = Poffset(self._core, self._base)
		return self._poffset

	@property
	def quadrature(self):
		"""quadrature commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_quadrature'):
			from .Rf_.Quadrature import Quadrature
			self._quadrature = Quadrature(self._core, self._base)
		return self._quadrature

	@property
	def skew(self):
		"""skew commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_skew'):
			from .Rf_.Skew import Skew
			self._skew = Skew(self._core, self._base)
		return self._skew

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Rf_.State import State
			self._state = State(self._core, self._base)
		return self._state
