from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.RepeatedCapability import RepeatedCapability
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class User:
	"""User commands group definition. 104 total commands, 25 Sub-groups, 0 group commands
	Repeated Capability: Channel, default value after init: Channel.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("user", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_channel_get', 'repcap_channel_set', repcap.Channel.Nr1)

	def clone(self) -> 'User':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = User(self._core, self._base.parent)
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
	def apm(self):
		"""apm commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_apm'):
			from .User_.Apm import Apm
			self._apm = Apm(self._core, self._base)
		return self._apm

	@property
	def asPy(self):
		"""asPy commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_asPy'):
			from .User_.AsPy import AsPy
			self._asPy = AsPy(self._core, self._base)
		return self._asPy

	@property
	def asrs(self):
		"""asrs commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_asrs'):
			from .User_.Asrs import Asrs
			self._asrs = Asrs(self._core, self._base)
		return self._asrs

	@property
	def ca(self):
		"""ca commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ca'):
			from .User_.Ca import Ca
			self._ca = Ca(self._core, self._base)
		return self._ca

	@property
	def caw(self):
		"""caw commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_caw'):
			from .User_.Caw import Caw
			self._caw = Caw(self._core, self._base)
		return self._caw

	@property
	def ccoding(self):
		"""ccoding commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ccoding'):
			from .User_.Ccoding import Ccoding
			self._ccoding = Ccoding(self._core, self._base)
		return self._ccoding

	@property
	def cell(self):
		"""cell commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_cell'):
			from .User_.Cell import Cell
			self._cell = Cell(self._core, self._base)
		return self._cell

	@property
	def data(self):
		"""data commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_data'):
			from .User_.Data import Data
			self._data = Data(self._core, self._base)
		return self._data

	@property
	def dselect(self):
		"""dselect commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dselect'):
			from .User_.Dselect import Dselect
			self._dselect = Dselect(self._core, self._base)
		return self._dselect

	@property
	def eimtarnti(self):
		"""eimtarnti commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_eimtarnti'):
			from .User_.Eimtarnti import Eimtarnti
			self._eimtarnti = Eimtarnti(self._core, self._base)
		return self._eimtarnti

	@property
	def epdcch(self):
		"""epdcch commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_epdcch'):
			from .User_.Epdcch import Epdcch
			self._epdcch = Epdcch(self._core, self._base)
		return self._epdcch

	@property
	def mcsTwo(self):
		"""mcsTwo commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_mcsTwo'):
			from .User_.McsTwo import McsTwo
			self._mcsTwo = McsTwo(self._core, self._base)
		return self._mcsTwo

	@property
	def niot(self):
		"""niot commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_niot'):
			from .User_.Niot import Niot
			self._niot = Niot(self._core, self._base)
		return self._niot

	@property
	def pa(self):
		"""pa commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pa'):
			from .User_.Pa import Pa
			self._pa = Pa(self._core, self._base)
		return self._pa

	@property
	def pattern(self):
		"""pattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pattern'):
			from .User_.Pattern import Pattern
			self._pattern = Pattern(self._core, self._base)
		return self._pattern

	@property
	def release(self):
		"""release commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_release'):
			from .User_.Release import Release
			self._release = Release(self._core, self._base)
		return self._release

	@property
	def scrambling(self):
		"""scrambling commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_scrambling'):
			from .User_.Scrambling import Scrambling
			self._scrambling = Scrambling(self._core, self._base)
		return self._scrambling

	@property
	def sps(self):
		"""sps commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_sps'):
			from .User_.Sps import Sps
			self._sps = Sps(self._core, self._base)
		return self._sps

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .User_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def sthp(self):
		"""sthp commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_sthp'):
			from .User_.Sthp import Sthp
			self._sthp = Sthp(self._core, self._base)
		return self._sthp

	@property
	def taltIndex(self):
		"""taltIndex commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_taltIndex'):
			from .User_.TaltIndex import TaltIndex
			self._taltIndex = TaltIndex(self._core, self._base)
		return self._taltIndex

	@property
	def txm(self):
		"""txm commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_txm'):
			from .User_.Txm import Txm
			self._txm = Txm(self._core, self._base)
		return self._txm

	@property
	def uec(self):
		"""uec commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_uec'):
			from .User_.Uec import Uec
			self._uec = Uec(self._core, self._base)
		return self._uec

	@property
	def ueid(self):
		"""ueid commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ueid'):
			from .User_.Ueid import Ueid
			self._ueid = Ueid(self._core, self._base)
		return self._ueid

	@property
	def ulca(self):
		"""ulca commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ulca'):
			from .User_.Ulca import Ulca
			self._ulca = Ulca(self._core, self._base)
		return self._ulca
