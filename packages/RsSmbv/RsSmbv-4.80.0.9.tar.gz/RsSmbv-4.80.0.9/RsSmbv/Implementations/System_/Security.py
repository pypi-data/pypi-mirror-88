from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Security:
	"""Security commands group definition. 17 total commands, 6 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("security", core, parent)

	def clone(self) -> 'Security':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Security(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def mmem(self):
		"""mmem commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_mmem'):
			from .Security_.Mmem import Mmem
			self._mmem = Mmem(self._core, self._base)
		return self._mmem

	@property
	def network(self):
		"""network commands group. 11 Sub-classes, 0 commands."""
		if not hasattr(self, '_network'):
			from .Security_.Network import Network
			self._network = Network(self._core, self._base)
		return self._network

	@property
	def sanitize(self):
		"""sanitize commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_sanitize'):
			from .Security_.Sanitize import Sanitize
			self._sanitize = Sanitize(self._core, self._base)
		return self._sanitize

	@property
	def suPolicy(self):
		"""suPolicy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_suPolicy'):
			from .Security_.SuPolicy import SuPolicy
			self._suPolicy = SuPolicy(self._core, self._base)
		return self._suPolicy

	@property
	def usbStorage(self):
		"""usbStorage commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_usbStorage'):
			from .Security_.UsbStorage import UsbStorage
			self._usbStorage = UsbStorage(self._core, self._base)
		return self._usbStorage

	@property
	def volMode(self):
		"""volMode commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_volMode'):
			from .Security_.VolMode import VolMode
			self._volMode = VolMode(self._core, self._base)
		return self._volMode

	def get_state(self) -> bool:
		"""SYSTem:SECurity:[STATe] \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('SYSTem:SECurity:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SYSTem:SECurity:[STATe] \n
		No command help available \n
			:param state: No help available
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SYSTem:SECurity:STATe {param}')
