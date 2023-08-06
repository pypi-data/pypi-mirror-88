from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dchannel:
	"""Dchannel commands group definition. 21 total commands, 7 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dchannel", core, parent)

	def clone(self) -> 'Dchannel':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Dchannel(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def clength(self):
		"""clength commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_clength'):
			from .Dchannel_.Clength import Clength
			self._clength = Clength(self._core, self._base)
		return self._clength

	@property
	def data(self):
		"""data commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_data'):
			from .Dchannel_.Data import Data
			self._data = Data(self._core, self._base)
		return self._data

	@property
	def drate(self):
		"""drate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_drate'):
			from .Dchannel_.Drate import Drate
			self._drate = Drate(self._core, self._base)
		return self._drate

	@property
	def fcs(self):
		"""fcs commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_fcs'):
			from .Dchannel_.Fcs import Fcs
			self._fcs = Fcs(self._core, self._base)
		return self._fcs

	@property
	def gain(self):
		"""gain commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_gain'):
			from .Dchannel_.Gain import Gain
			self._gain = Gain(self._core, self._base)
		return self._gain

	@property
	def packet(self):
		"""packet commands group. 11 Sub-classes, 0 commands."""
		if not hasattr(self, '_packet'):
			from .Dchannel_.Packet import Packet
			self._packet = Packet(self._core, self._base)
		return self._packet

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Dchannel_.State import State
			self._state = State(self._core, self._base)
		return self._state
