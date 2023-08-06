from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Plcch:
	"""Plcch commands group definition. 3 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("plcch", core, parent)

	def clone(self) -> 'Plcch':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Plcch(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def ssPattern(self):
		"""ssPattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ssPattern'):
			from .Plcch_.SsPattern import SsPattern
			self._ssPattern = SsPattern(self._core, self._base)
		return self._ssPattern

	@property
	def tpcPattern(self):
		"""tpcPattern commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tpcPattern'):
			from .Plcch_.TpcPattern import TpcPattern
			self._tpcPattern = TpcPattern(self._core, self._base)
		return self._tpcPattern

	@property
	def ttInterval(self):
		"""ttInterval commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ttInterval'):
			from .Plcch_.TtInterval import TtInterval
			self._ttInterval = TtInterval(self._core, self._base)
		return self._ttInterval
