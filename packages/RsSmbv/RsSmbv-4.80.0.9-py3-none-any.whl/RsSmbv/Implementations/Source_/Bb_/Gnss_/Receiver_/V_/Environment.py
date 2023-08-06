from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Environment:
	"""Environment commands group definition. 43 total commands, 7 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("environment", core, parent)

	def clone(self) -> 'Environment':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Environment(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def full(self):
		"""full commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_full'):
			from .Environment_.Full import Full
			self._full = Full(self._core, self._base)
		return self._full

	@property
	def gsr(self):
		"""gsr commands group. 11 Sub-classes, 0 commands."""
		if not hasattr(self, '_gsr'):
			from .Environment_.Gsr import Gsr
			self._gsr = Gsr(self._core, self._base)
		return self._gsr

	@property
	def lmm(self):
		"""lmm commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_lmm'):
			from .Environment_.Lmm import Lmm
			self._lmm = Lmm(self._core, self._base)
		return self._lmm

	@property
	def mpath(self):
		"""mpath commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_mpath'):
			from .Environment_.Mpath import Mpath
			self._mpath = Mpath(self._core, self._base)
		return self._mpath

	@property
	def rpl(self):
		"""rpl commands group. 7 Sub-classes, 0 commands."""
		if not hasattr(self, '_rpl'):
			from .Environment_.Rpl import Rpl
			self._rpl = Rpl(self._core, self._base)
		return self._rpl

	@property
	def vobs(self):
		"""vobs commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_vobs'):
			from .Environment_.Vobs import Vobs
			self._vobs = Vobs(self._core, self._base)
		return self._vobs

	@property
	def model(self):
		"""model commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_model'):
			from .Environment_.Model import Model
			self._model = Model(self._core, self._base)
		return self._model
