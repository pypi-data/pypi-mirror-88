from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.RepeatedCapability import RepeatedCapability
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Alloc:
	"""Alloc commands group definition. 38 total commands, 19 Sub-groups, 0 group commands
	Repeated Capability: Channel, default value after init: Channel.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("alloc", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_channel_get', 'repcap_channel_set', repcap.Channel.Nr1)

	def clone(self) -> 'Alloc':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Alloc(self._core, self._base.parent)
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
	def absFrames(self):
		"""absFrames commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_absFrames'):
			from .Alloc_.AbsFrames import AbsFrames
			self._absFrames = AbsFrames(self._core, self._base)
		return self._absFrames

	@property
	def ccoding(self):
		"""ccoding commands group. 9 Sub-classes, 0 commands."""
		if not hasattr(self, '_ccoding'):
			from .Alloc_.Ccoding import Ccoding
			self._ccoding = Ccoding(self._core, self._base)
		return self._ccoding

	@property
	def codewords(self):
		"""codewords commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_codewords'):
			from .Alloc_.Codewords import Codewords
			self._codewords = Codewords(self._core, self._base)
		return self._codewords

	@property
	def conflict(self):
		"""conflict commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_conflict'):
			from .Alloc_.Conflict import Conflict
			self._conflict = Conflict(self._core, self._base)
		return self._conflict

	@property
	def conType(self):
		"""conType commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_conType'):
			from .Alloc_.ConType import ConType
			self._conType = ConType(self._core, self._base)
		return self._conType

	@property
	def data(self):
		"""data commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_data'):
			from .Alloc_.Data import Data
			self._data = Data(self._core, self._base)
		return self._data

	@property
	def dselect(self):
		"""dselect commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dselect'):
			from .Alloc_.Dselect import Dselect
			self._dselect = Dselect(self._core, self._base)
		return self._dselect

	@property
	def modulation(self):
		"""modulation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_modulation'):
			from .Alloc_.Modulation import Modulation
			self._modulation = Modulation(self._core, self._base)
		return self._modulation

	@property
	def norb(self):
		"""norb commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_norb'):
			from .Alloc_.Norb import Norb
			self._norb = Norb(self._core, self._base)
		return self._norb

	@property
	def ovrb(self):
		"""ovrb commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ovrb'):
			from .Alloc_.Ovrb import Ovrb
			self._ovrb = Ovrb(self._core, self._base)
		return self._ovrb

	@property
	def pattern(self):
		"""pattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pattern'):
			from .Alloc_.Pattern import Pattern
			self._pattern = Pattern(self._core, self._base)
		return self._pattern

	@property
	def physBits(self):
		"""physBits commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_physBits'):
			from .Alloc_.PhysBits import PhysBits
			self._physBits = PhysBits(self._core, self._base)
		return self._physBits

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .Alloc_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power

	@property
	def precoding(self):
		"""precoding commands group. 9 Sub-classes, 0 commands."""
		if not hasattr(self, '_precoding'):
			from .Alloc_.Precoding import Precoding
			self._precoding = Precoding(self._core, self._base)
		return self._precoding

	@property
	def scrambling(self):
		"""scrambling commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_scrambling'):
			from .Alloc_.Scrambling import Scrambling
			self._scrambling = Scrambling(self._core, self._base)
		return self._scrambling

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Alloc_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def stnb(self):
		"""stnb commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_stnb'):
			from .Alloc_.Stnb import Stnb
			self._stnb = Stnb(self._core, self._base)
		return self._stnb

	@property
	def stsFrame(self):
		"""stsFrame commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_stsFrame'):
			from .Alloc_.StsFrame import StsFrame
			self._stsFrame = StsFrame(self._core, self._base)
		return self._stsFrame

	@property
	def stSymbol(self):
		"""stSymbol commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_stSymbol'):
			from .Alloc_.StSymbol import StSymbol
			self._stSymbol = StSymbol(self._core, self._base)
		return self._stSymbol
