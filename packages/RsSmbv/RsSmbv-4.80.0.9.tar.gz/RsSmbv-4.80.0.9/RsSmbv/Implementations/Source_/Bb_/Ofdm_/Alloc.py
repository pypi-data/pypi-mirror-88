from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.RepeatedCapability import RepeatedCapability
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Alloc:
	"""Alloc commands group definition. 20 total commands, 15 Sub-groups, 0 group commands
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
	def ciqfile(self):
		"""ciqfile commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ciqfile'):
			from .Alloc_.Ciqfile import Ciqfile
			self._ciqfile = Ciqfile(self._core, self._base)
		return self._ciqfile

	@property
	def conflict(self):
		"""conflict commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_conflict'):
			from .Alloc_.Conflict import Conflict
			self._conflict = Conflict(self._core, self._base)
		return self._conflict

	@property
	def content(self):
		"""content commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_content'):
			from .Alloc_.Content import Content
			self._content = Content(self._core, self._base)
		return self._content

	@property
	def data(self):
		"""data commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_data'):
			from .Alloc_.Data import Data
			self._data = Data(self._core, self._base)
		return self._data

	@property
	def listPy(self):
		"""listPy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_listPy'):
			from .Alloc_.ListPy import ListPy
			self._listPy = ListPy(self._core, self._base)
		return self._listPy

	@property
	def modulation(self):
		"""modulation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_modulation'):
			from .Alloc_.Modulation import Modulation
			self._modulation = Modulation(self._core, self._base)
		return self._modulation

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
	def pwr(self):
		"""pwr commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pwr'):
			from .Alloc_.Pwr import Pwr
			self._pwr = Pwr(self._core, self._base)
		return self._pwr

	@property
	def scma(self):
		"""scma commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_scma'):
			from .Alloc_.Scma import Scma
			self._scma = Scma(self._core, self._base)
		return self._scma

	@property
	def scno(self):
		"""scno commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scno'):
			from .Alloc_.Scno import Scno
			self._scno = Scno(self._core, self._base)
		return self._scno

	@property
	def scOffset(self):
		"""scOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scOffset'):
			from .Alloc_.ScOffset import ScOffset
			self._scOffset = ScOffset(self._core, self._base)
		return self._scOffset

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Alloc_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def syno(self):
		"""syno commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_syno'):
			from .Alloc_.Syno import Syno
			self._syno = Syno(self._core, self._base)
		return self._syno

	@property
	def syOffset(self):
		"""syOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_syOffset'):
			from .Alloc_.SyOffset import SyOffset
			self._syOffset = SyOffset(self._core, self._base)
		return self._syOffset
