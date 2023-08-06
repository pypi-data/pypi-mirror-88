from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BfConfiguration:
	"""BfConfiguration commands group definition. 27 total commands, 9 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("bfConfiguration", core, parent)

	def clone(self) -> 'BfConfiguration':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = BfConfiguration(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def binterval(self):
		"""binterval commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_binterval'):
			from .BfConfiguration_.Binterval import Binterval
			self._binterval = Binterval(self._core, self._base)
		return self._binterval

	@property
	def capability(self):
		"""capability commands group. 16 Sub-classes, 0 commands."""
		if not hasattr(self, '_capability'):
			from .BfConfiguration_.Capability import Capability
			self._capability = Capability(self._core, self._base)
		return self._capability

	@property
	def dcChannel(self):
		"""dcChannel commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dcChannel'):
			from .BfConfiguration_.DcChannel import DcChannel
			self._dcChannel = DcChannel(self._core, self._base)
		return self._dcChannel

	@property
	def erp(self):
		"""erp commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_erp'):
			from .BfConfiguration_.Erp import Erp
			self._erp = Erp(self._core, self._base)
		return self._erp

	@property
	def htCapability(self):
		"""htCapability commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_htCapability'):
			from .BfConfiguration_.HtCapability import HtCapability
			self._htCapability = HtCapability(self._core, self._base)
		return self._htCapability

	@property
	def iaWindow(self):
		"""iaWindow commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_iaWindow'):
			from .BfConfiguration_.IaWindow import IaWindow
			self._iaWindow = IaWindow(self._core, self._base)
		return self._iaWindow

	@property
	def symbolRate(self):
		"""symbolRate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_symbolRate'):
			from .BfConfiguration_.SymbolRate import SymbolRate
			self._symbolRate = SymbolRate(self._core, self._base)
		return self._symbolRate

	@property
	def ssid(self):
		"""ssid commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ssid'):
			from .BfConfiguration_.Ssid import Ssid
			self._ssid = Ssid(self._core, self._base)
		return self._ssid

	@property
	def tstamp(self):
		"""tstamp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tstamp'):
			from .BfConfiguration_.Tstamp import Tstamp
			self._tstamp = Tstamp(self._core, self._base)
		return self._tstamp
