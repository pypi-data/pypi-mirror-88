from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.RepeatedCapability import RepeatedCapability
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pmch:
	"""Pmch commands group definition. 10 total commands, 10 Sub-groups, 0 group commands
	Repeated Capability: Channel, default value after init: Channel.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pmch", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_channel_get', 'repcap_channel_set', repcap.Channel.Nr1)

	def clone(self) -> 'Pmch':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Pmch(self._core, self._base.parent)
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
		"""data commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_data'):
			from .Pmch_.Data import Data
			self._data = Data(self._core, self._base)
		return self._data

	@property
	def dlist(self):
		"""dlist commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dlist'):
			from .Pmch_.Dlist import Dlist
			self._dlist = Dlist(self._core, self._base)
		return self._dlist

	@property
	def mcs(self):
		"""mcs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mcs'):
			from .Pmch_.Mcs import Mcs
			self._mcs = Mcs(self._core, self._base)
		return self._mcs

	@property
	def mcsTwo(self):
		"""mcsTwo commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mcsTwo'):
			from .Pmch_.McsTwo import McsTwo
			self._mcsTwo = McsTwo(self._core, self._base)
		return self._mcsTwo

	@property
	def mod(self):
		"""mod commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mod'):
			from .Pmch_.Mod import Mod
			self._mod = Mod(self._core, self._base)
		return self._mod

	@property
	def pattern(self):
		"""pattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pattern'):
			from .Pmch_.Pattern import Pattern
			self._pattern = Pattern(self._core, self._base)
		return self._pattern

	@property
	def saEnd(self):
		"""saEnd commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_saEnd'):
			from .Pmch_.SaEnd import SaEnd
			self._saEnd = SaEnd(self._core, self._base)
		return self._saEnd

	@property
	def saStart(self):
		"""saStart commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_saStart'):
			from .Pmch_.SaStart import SaStart
			self._saStart = SaStart(self._core, self._base)
		return self._saStart

	@property
	def speriod(self):
		"""speriod commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_speriod'):
			from .Pmch_.Speriod import Speriod
			self._speriod = Speriod(self._core, self._base)
		return self._speriod

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Pmch_.State import State
			self._state = State(self._core, self._base)
		return self._state
