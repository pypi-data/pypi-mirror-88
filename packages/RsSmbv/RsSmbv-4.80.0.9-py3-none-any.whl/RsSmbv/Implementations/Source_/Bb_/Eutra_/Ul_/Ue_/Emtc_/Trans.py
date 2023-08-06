from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.RepeatedCapability import RepeatedCapability
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Trans:
	"""Trans commands group definition. 32 total commands, 23 Sub-groups, 0 group commands
	Repeated Capability: Channel, default value after init: Channel.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("trans", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_channel_get', 'repcap_channel_set', repcap.Channel.Nr1)

	def clone(self) -> 'Trans':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Trans(self._core, self._base.parent)
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
	def asFrame(self):
		"""asFrame commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_asFrame'):
			from .Trans_.AsFrame import AsFrame
			self._asFrame = AsFrame(self._core, self._base)
		return self._asFrame

	@property
	def ccoding(self):
		"""ccoding commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_ccoding'):
			from .Trans_.Ccoding import Ccoding
			self._ccoding = Ccoding(self._core, self._base)
		return self._ccoding

	@property
	def content(self):
		"""content commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_content'):
			from .Trans_.Content import Content
			self._content = Content(self._core, self._base)
		return self._content

	@property
	def drs(self):
		"""drs commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_drs'):
			from .Trans_.Drs import Drs
			self._drs = Drs(self._core, self._base)
		return self._drs

	@property
	def formatPy(self):
		"""formatPy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_formatPy'):
			from .Trans_.FormatPy import FormatPy
			self._formatPy = FormatPy(self._core, self._base)
		return self._formatPy

	@property
	def harq(self):
		"""harq commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_harq'):
			from .Trans_.Harq import Harq
			self._harq = Harq(self._core, self._base)
		return self._harq

	@property
	def modulation(self):
		"""modulation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_modulation'):
			from .Trans_.Modulation import Modulation
			self._modulation = Modulation(self._core, self._base)
		return self._modulation

	@property
	def napUsed(self):
		"""napUsed commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_napUsed'):
			from .Trans_.NapUsed import NapUsed
			self._napUsed = NapUsed(self._core, self._base)
		return self._napUsed

	@property
	def ndmrs(self):
		"""ndmrs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ndmrs'):
			from .Trans_.Ndmrs import Ndmrs
			self._ndmrs = Ndmrs(self._core, self._base)
		return self._ndmrs

	@property
	def npucch(self):
		"""npucch commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_npucch'):
			from .Trans_.Npucch import Npucch
			self._npucch = Npucch(self._core, self._base)
		return self._npucch

	@property
	def nrBlocks(self):
		"""nrBlocks commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nrBlocks'):
			from .Trans_.NrBlocks import NrBlocks
			self._nrBlocks = NrBlocks(self._core, self._base)
		return self._nrBlocks

	@property
	def physBits(self):
		"""physBits commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_physBits'):
			from .Trans_.PhysBits import PhysBits
			self._physBits = PhysBits(self._core, self._base)
		return self._physBits

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .Trans_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power

	@property
	def pucch(self):
		"""pucch commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_pucch'):
			from .Trans_.Pucch import Pucch
			self._pucch = Pucch(self._core, self._base)
		return self._pucch

	@property
	def pusch(self):
		"""pusch commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_pusch'):
			from .Trans_.Pusch import Pusch
			self._pusch = Pusch(self._core, self._base)
		return self._pusch

	@property
	def rbOffset(self):
		"""rbOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rbOffset'):
			from .Trans_.RbOffset import RbOffset
			self._rbOffset = RbOffset(self._core, self._base)
		return self._rbOffset

	@property
	def repetitions(self):
		"""repetitions commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_repetitions'):
			from .Trans_.Repetitions import Repetitions
			self._repetitions = Repetitions(self._core, self._base)
		return self._repetitions

	@property
	def stnBand(self):
		"""stnBand commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_stnBand'):
			from .Trans_.StnBand import StnBand
			self._stnBand = StnBand(self._core, self._base)
		return self._stnBand

	@property
	def stsFrame(self):
		"""stsFrame commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_stsFrame'):
			from .Trans_.StsFrame import StsFrame
			self._stsFrame = StsFrame(self._core, self._base)
		return self._stsFrame

	@property
	def stwBand(self):
		"""stwBand commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_stwBand'):
			from .Trans_.StwBand import StwBand
			self._stwBand = StwBand(self._core, self._base)
		return self._stwBand

	@property
	def ulsch(self):
		"""ulsch commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ulsch'):
			from .Trans_.Ulsch import Ulsch
			self._ulsch = Ulsch(self._core, self._base)
		return self._ulsch

	@property
	def wbrbOffset(self):
		"""wbrbOffset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_wbrbOffset'):
			from .Trans_.WbrbOffset import WbrbOffset
			self._wbrbOffset = WbrbOffset(self._core, self._base)
		return self._wbrbOffset

	@property
	def wrBlocks(self):
		"""wrBlocks commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_wrBlocks'):
			from .Trans_.WrBlocks import WrBlocks
			self._wrBlocks = WrBlocks(self._core, self._base)
		return self._wrBlocks
