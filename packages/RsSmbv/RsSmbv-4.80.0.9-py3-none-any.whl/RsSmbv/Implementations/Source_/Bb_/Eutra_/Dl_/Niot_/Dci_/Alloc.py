from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.RepeatedCapability import RepeatedCapability
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Alloc:
	"""Alloc commands group definition. 34 total commands, 28 Sub-groups, 0 group commands
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
	def bits(self):
		"""bits commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bits'):
			from .Alloc_.Bits import Bits
			self._bits = Bits(self._core, self._base)
		return self._bits

	@property
	def cces(self):
		"""cces commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cces'):
			from .Alloc_.Cces import Cces
			self._cces = Cces(self._core, self._base)
		return self._cces

	@property
	def conflict(self):
		"""conflict commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_conflict'):
			from .Alloc_.Conflict import Conflict
			self._conflict = Conflict(self._core, self._base)
		return self._conflict

	@property
	def dist(self):
		"""dist commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dist'):
			from .Alloc_.Dist import Dist
			self._dist = Dist(self._core, self._base)
		return self._dist

	@property
	def fmt(self):
		"""fmt commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fmt'):
			from .Alloc_.Fmt import Fmt
			self._fmt = Fmt(self._core, self._base)
		return self._fmt

	@property
	def hack(self):
		"""hack commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hack'):
			from .Alloc_.Hack import Hack
			self._hack = Hack(self._core, self._base)
		return self._hack

	@property
	def hpNumber(self):
		"""hpNumber commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hpNumber'):
			from .Alloc_.HpNumber import HpNumber
			self._hpNumber = HpNumber(self._core, self._base)
		return self._hpNumber

	@property
	def idcce(self):
		"""idcce commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_idcce'):
			from .Alloc_.Idcce import Idcce
			self._idcce = Idcce(self._core, self._base)
		return self._idcce

	@property
	def idelay(self):
		"""idelay commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_idelay'):
			from .Alloc_.Idelay import Idelay
			self._idelay = Idelay(self._core, self._base)
		return self._idelay

	@property
	def iru(self):
		"""iru commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_iru'):
			from .Alloc_.Iru import Iru
			self._iru = Iru(self._core, self._base)
		return self._iru

	@property
	def mcScheme(self):
		"""mcScheme commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mcScheme'):
			from .Alloc_.McScheme import McScheme
			self._mcScheme = McScheme(self._core, self._base)
		return self._mcScheme

	@property
	def ndind(self):
		"""ndind commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ndind'):
			from .Alloc_.Ndind import Ndind
			self._ndind = Ndind(self._core, self._base)
		return self._ndind

	@property
	def npdcch(self):
		"""npdcch commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_npdcch'):
			from .Alloc_.Npdcch import Npdcch
			self._npdcch = Npdcch(self._core, self._base)
		return self._npdcch

	@property
	def npdsch(self):
		"""npdsch commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_npdsch'):
			from .Alloc_.Npdsch import Npdsch
			self._npdsch = Npdsch(self._core, self._base)
		return self._npdsch

	@property
	def nprach(self):
		"""nprach commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_nprach'):
			from .Alloc_.Nprach import Nprach
			self._nprach = Nprach(self._core, self._base)
		return self._nprach

	@property
	def npusch(self):
		"""npusch commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_npusch'):
			from .Alloc_.Npusch import Npusch
			self._npusch = Npusch(self._core, self._base)
		return self._npusch

	@property
	def nrUnits(self):
		"""nrUnits commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nrUnits'):
			from .Alloc_.NrUnits import NrUnits
			self._nrUnits = NrUnits(self._core, self._base)
		return self._nrUnits

	@property
	def pag(self):
		"""pag commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pag'):
			from .Alloc_.Pag import Pag
			self._pag = Pag(self._core, self._base)
		return self._pag

	@property
	def rversion(self):
		"""rversion commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rversion'):
			from .Alloc_.Rversion import Rversion
			self._rversion = Rversion(self._core, self._base)
		return self._rversion

	@property
	def scind(self):
		"""scind commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_scind'):
			from .Alloc_.Scind import Scind
			self._scind = Scind(self._core, self._base)
		return self._scind

	@property
	def sfrpt(self):
		"""sfrpt commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sfrpt'):
			from .Alloc_.Sfrpt import Sfrpt
			self._sfrpt = Sfrpt(self._core, self._base)
		return self._sfrpt

	@property
	def sime(self):
		"""sime commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sime'):
			from .Alloc_.Sime import Sime
			self._sime = Sime(self._core, self._base)
		return self._sime

	@property
	def sinf(self):
		"""sinf commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sinf'):
			from .Alloc_.Sinf import Sinf
			self._sinf = Sinf(self._core, self._base)
		return self._sinf

	@property
	def ssp(self):
		"""ssp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ssp'):
			from .Alloc_.Ssp import Ssp
			self._ssp = Ssp(self._core, self._base)
		return self._ssp

	@property
	def stsFrame(self):
		"""stsFrame commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_stsFrame'):
			from .Alloc_.StsFrame import StsFrame
			self._stsFrame = StsFrame(self._core, self._base)
		return self._stsFrame

	@property
	def tbsz(self):
		"""tbsz commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tbsz'):
			from .Alloc_.Tbsz import Tbsz
			self._tbsz = Tbsz(self._core, self._base)
		return self._tbsz

	@property
	def ueid(self):
		"""ueid commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ueid'):
			from .Alloc_.Ueid import Ueid
			self._ueid = Ueid(self._core, self._base)
		return self._ueid

	@property
	def user(self):
		"""user commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_user'):
			from .Alloc_.User import User
			self._user = User(self._core, self._base)
		return self._user
