from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.RepeatedCapability import RepeatedCapability
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Cw:
	"""Cw commands group definition. 30 total commands, 18 Sub-groups, 0 group commands
	Repeated Capability: Codeword, default value after init: Codeword.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cw", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_codeword_get', 'repcap_codeword_set', repcap.Codeword.Nr0)

	def clone(self) -> 'Cw':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Cw(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	def repcap_codeword_set(self, enum_value: repcap.Codeword) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Codeword.Default
		Default value after init: Codeword.Nr0"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_codeword_get(self) -> repcap.Codeword:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def aoc(self):
		"""aoc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_aoc'):
			from .Cw_.Aoc import Aoc
			self._aoc = Aoc(self._core, self._base)
		return self._aoc

	@property
	def ccoding(self):
		"""ccoding commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_ccoding'):
			from .Cw_.Ccoding import Ccoding
			self._ccoding = Ccoding(self._core, self._base)
		return self._ccoding

	@property
	def conflict(self):
		"""conflict commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_conflict'):
			from .Cw_.Conflict import Conflict
			self._conflict = Conflict(self._core, self._base)
		return self._conflict

	@property
	def conType(self):
		"""conType commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_conType'):
			from .Cw_.ConType import ConType
			self._conType = ConType(self._core, self._base)
		return self._conType

	@property
	def data(self):
		"""data commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_data'):
			from .Cw_.Data import Data
			self._data = Data(self._core, self._base)
		return self._data

	@property
	def dselect(self):
		"""dselect commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dselect'):
			from .Cw_.Dselect import Dselect
			self._dselect = Dselect(self._core, self._base)
		return self._dselect

	@property
	def gap(self):
		"""gap commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_gap'):
			from .Cw_.Gap import Gap
			self._gap = Gap(self._core, self._base)
		return self._gap

	@property
	def modulation(self):
		"""modulation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_modulation'):
			from .Cw_.Modulation import Modulation
			self._modulation = Modulation(self._core, self._base)
		return self._modulation

	@property
	def pattern(self):
		"""pattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pattern'):
			from .Cw_.Pattern import Pattern
			self._pattern = Pattern(self._core, self._base)
		return self._pattern

	@property
	def physBits(self):
		"""physBits commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_physBits'):
			from .Cw_.PhysBits import PhysBits
			self._physBits = PhysBits(self._core, self._base)
		return self._physBits

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .Cw_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power

	@property
	def precoding(self):
		"""precoding commands group. 9 Sub-classes, 0 commands."""
		if not hasattr(self, '_precoding'):
			from .Cw_.Precoding import Precoding
			self._precoding = Precoding(self._core, self._base)
		return self._precoding

	@property
	def rbCount(self):
		"""rbCount commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rbCount'):
			from .Cw_.RbCount import RbCount
			self._rbCount = RbCount(self._core, self._base)
		return self._rbCount

	@property
	def rbOffset(self):
		"""rbOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rbOffset'):
			from .Cw_.RbOffset import RbOffset
			self._rbOffset = RbOffset(self._core, self._base)
		return self._rbOffset

	@property
	def scrambling(self):
		"""scrambling commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_scrambling'):
			from .Cw_.Scrambling import Scrambling
			self._scrambling = Scrambling(self._core, self._base)
		return self._scrambling

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Cw_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def symCount(self):
		"""symCount commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_symCount'):
			from .Cw_.SymCount import SymCount
			self._symCount = SymCount(self._core, self._base)
		return self._symCount

	@property
	def symOffset(self):
		"""symOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_symOffset'):
			from .Cw_.SymOffset import SymOffset
			self._symOffset = SymOffset(self._core, self._base)
		return self._symOffset
