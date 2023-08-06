from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Niot:
	"""Niot commands group definition. 5 total commands, 5 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("niot", core, parent)

	def clone(self) -> 'Niot':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Niot(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def config(self):
		"""config commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_config'):
			from .Niot_.Config import Config
			self._config = Config(self._core, self._base)
		return self._config

	@property
	def init(self):
		"""init commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_init'):
			from .Niot_.Init import Init
			self._init = Init(self._core, self._base)
		return self._init

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .Niot_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power

	@property
	def sfStart(self):
		"""sfStart commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sfStart'):
			from .Niot_.SfStart import SfStart
			self._sfStart = SfStart(self._core, self._base)
		return self._sfStart

	@property
	def strt(self):
		"""strt commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_strt'):
			from .Niot_.Strt import Strt
			self._strt = Strt(self._core, self._base)
		return self._strt
