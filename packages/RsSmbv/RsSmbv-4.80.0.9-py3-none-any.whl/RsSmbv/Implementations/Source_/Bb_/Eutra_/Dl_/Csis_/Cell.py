from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.RepeatedCapability import RepeatedCapability
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Cell:
	"""Cell commands group definition. 17 total commands, 14 Sub-groups, 0 group commands
	Repeated Capability: Channel, default value after init: Channel.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cell", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_channel_get', 'repcap_channel_set', repcap.Channel.Nr1)

	def clone(self) -> 'Cell':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Cell(self._core, self._base.parent)
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
	def cdmType(self):
		"""cdmType commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cdmType'):
			from .Cell_.CdmType import CdmType
			self._cdmType = CdmType(self._core, self._base)
		return self._cdmType

	@property
	def config(self):
		"""config commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_config'):
			from .Cell_.Config import Config
			self._config = Config(self._core, self._base)
		return self._config

	@property
	def dwpts(self):
		"""dwpts commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dwpts'):
			from .Cell_.Dwpts import Dwpts
			self._dwpts = Dwpts(self._core, self._base)
		return self._dwpts

	@property
	def frDensity(self):
		"""frDensity commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_frDensity'):
			from .Cell_.FrDensity import FrDensity
			self._frDensity = FrDensity(self._core, self._base)
		return self._frDensity

	@property
	def nap(self):
		"""nap commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nap'):
			from .Cell_.Nap import Nap
			self._nap = Nap(self._core, self._base)
		return self._nap

	@property
	def ncfg(self):
		"""ncfg commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ncfg'):
			from .Cell_.Ncfg import Ncfg
			self._ncfg = Ncfg(self._core, self._base)
		return self._ncfg

	@property
	def pow(self):
		"""pow commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pow'):
			from .Cell_.Pow import Pow
			self._pow = Pow(self._core, self._base)
		return self._pow

	@property
	def scid(self):
		"""scid commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scid'):
			from .Cell_.Scid import Scid
			self._scid = Scid(self._core, self._base)
		return self._scid

	@property
	def sfDelta(self):
		"""sfDelta commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sfDelta'):
			from .Cell_.SfDelta import SfDelta
			self._sfDelta = SfDelta(self._core, self._base)
		return self._sfDelta

	@property
	def sfi(self):
		"""sfi commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sfi'):
			from .Cell_.Sfi import Sfi
			self._sfi = Sfi(self._core, self._base)
		return self._sfi

	@property
	def sft(self):
		"""sft commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sft'):
			from .Cell_.Sft import Sft
			self._sft = Sft(self._core, self._base)
		return self._sft

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Cell_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def transcomb(self):
		"""transcomb commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_transcomb'):
			from .Cell_.Transcomb import Transcomb
			self._transcomb = Transcomb(self._core, self._base)
		return self._transcomb

	@property
	def zprs(self):
		"""zprs commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_zprs'):
			from .Cell_.Zprs import Zprs
			self._zprs = Zprs(self._core, self._base)
		return self._zprs
