from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.RepeatedCapability import RepeatedCapability
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class User:
	"""User commands group definition. 83 total commands, 20 Sub-groups, 0 group commands
	Repeated Capability: AvailableUser, default value after init: AvailableUser.Nr0"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("user", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_availableUser_get', 'repcap_availableUser_set', repcap.AvailableUser.Nr0)

	def clone(self) -> 'User':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = User(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	def repcap_availableUser_set(self, enum_value: repcap.AvailableUser) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to AvailableUser.Default
		Default value after init: AvailableUser.Nr0"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_availableUser_get(self) -> repcap.AvailableUser:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def dcm(self):
		"""dcm commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dcm'):
			from .User_.Dcm import Dcm
			self._dcm = Dcm(self._core, self._base)
		return self._dcm

	@property
	def gain(self):
		"""gain commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_gain'):
			from .User_.Gain import Gain
			self._gain = Gain(self._core, self._base)
		return self._gain

	@property
	def muMimo(self):
		"""muMimo commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_muMimo'):
			from .User_.MuMimo import MuMimo
			self._muMimo = MuMimo(self._core, self._base)
		return self._muMimo

	@property
	def nsts(self):
		"""nsts commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nsts'):
			from .User_.Nsts import Nsts
			self._nsts = Nsts(self._core, self._base)
		return self._nsts

	@property
	def rutype(self):
		"""rutype commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rutype'):
			from .User_.Rutype import Rutype
			self._rutype = Rutype(self._core, self._base)
		return self._rutype

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .User_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def staid(self):
		"""staid commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_staid'):
			from .User_.Staid import Staid
			self._staid = Staid(self._core, self._base)
		return self._staid

	@property
	def txBf(self):
		"""txBf commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_txBf'):
			from .User_.TxBf import TxBf
			self._txBf = TxBf(self._core, self._base)
		return self._txBf

	@property
	def coding(self):
		"""coding commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_coding'):
			from .User_.Coding import Coding
			self._coding = Coding(self._core, self._base)
		return self._coding

	@property
	def data(self):
		"""data commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_data'):
			from .User_.Data import Data
			self._data = Data(self._core, self._base)
		return self._data

	@property
	def dpnSeed(self):
		"""dpnSeed commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_dpnSeed'):
			from .User_.DpnSeed import DpnSeed
			self._dpnSeed = DpnSeed(self._core, self._base)
		return self._dpnSeed

	@property
	def ileaver(self):
		"""ileaver commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ileaver'):
			from .User_.Ileaver import Ileaver
			self._ileaver = Ileaver(self._core, self._base)
		return self._ileaver

	@property
	def mac(self):
		"""mac commands group. 10 Sub-classes, 0 commands."""
		if not hasattr(self, '_mac'):
			from .User_.Mac import Mac
			self._mac = Mac(self._core, self._base)
		return self._mac

	@property
	def mcs(self):
		"""mcs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mcs'):
			from .User_.Mcs import Mcs
			self._mcs = Mcs(self._core, self._base)
		return self._mcs

	@property
	def modulation(self):
		"""modulation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_modulation'):
			from .User_.Modulation import Modulation
			self._modulation = Modulation(self._core, self._base)
		return self._modulation

	@property
	def mpdu(self):
		"""mpdu commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_mpdu'):
			from .User_.Mpdu import Mpdu
			self._mpdu = Mpdu(self._core, self._base)
		return self._mpdu

	@property
	def pnSeed(self):
		"""pnSeed commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pnSeed'):
			from .User_.PnSeed import PnSeed
			self._pnSeed = PnSeed(self._core, self._base)
		return self._pnSeed

	@property
	def scrambler(self):
		"""scrambler commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_scrambler'):
			from .User_.Scrambler import Scrambler
			self._scrambler = Scrambler(self._core, self._base)
		return self._scrambler

	@property
	def service(self):
		"""service commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_service'):
			from .User_.Service import Service
			self._service = Service(self._core, self._base)
		return self._service

	@property
	def tfConfig(self):
		"""tfConfig commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_tfConfig'):
			from .User_.TfConfig import TfConfig
			self._tfConfig = TfConfig(self._core, self._base)
		return self._tfConfig
