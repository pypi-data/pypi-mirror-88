from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Data:
	"""Data commands group definition. 8 total commands, 2 Sub-groups, 6 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("data", core, parent)

	def clone(self) -> 'Data':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Data(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def error(self):
		"""error commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_error'):
			from .Data_.Error import Error
			self._error = Error(self._core, self._base)
		return self._error

	@property
	def trigger(self):
		"""trigger commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_trigger'):
			from .Data_.Trigger import Trigger
			self._trigger = Trigger(self._core, self._base)
		return self._trigger

	def get_frequency(self) -> int:
		"""TEST:BB:DATA:FREQuency \n
		No command help available \n
			:return: clock: No help available
		"""
		response = self._core.io.query_str('TEST:BB:DATA:FREQuency?')
		return Conversions.str_to_int(response)

	def set_frequency(self, clock: int) -> None:
		"""TEST:BB:DATA:FREQuency \n
		No command help available \n
			:param clock: No help available
		"""
		param = Conversions.decimal_value_to_str(clock)
		self._core.io.write(f'TEST:BB:DATA:FREQuency {param}')

	def get_off_time(self) -> int:
		"""TEST:BB:DATA:OFFTime \n
		No command help available \n
			:return: off_time: No help available
		"""
		response = self._core.io.query_str('TEST:BB:DATA:OFFTime?')
		return Conversions.str_to_int(response)

	def set_off_time(self, off_time: int) -> None:
		"""TEST:BB:DATA:OFFTime \n
		No command help available \n
			:param off_time: No help available
		"""
		param = Conversions.decimal_value_to_str(off_time)
		self._core.io.write(f'TEST:BB:DATA:OFFTime {param}')

	def get_ontime(self) -> int:
		"""TEST:BB:DATA:ONTime \n
		No command help available \n
			:return: on_time: No help available
		"""
		response = self._core.io.query_str('TEST:BB:DATA:ONTime?')
		return Conversions.str_to_int(response)

	def set_ontime(self, on_time: int) -> None:
		"""TEST:BB:DATA:ONTime \n
		No command help available \n
			:param on_time: No help available
		"""
		param = Conversions.decimal_value_to_str(on_time)
		self._core.io.write(f'TEST:BB:DATA:ONTime {param}')

	def get_rdelay(self) -> int:
		"""TEST:BB:DATA:RDELay \n
		No command help available \n
			:return: restart_delay: No help available
		"""
		response = self._core.io.query_str('TEST:BB:DATA:RDELay?')
		return Conversions.str_to_int(response)

	def set_rdelay(self, restart_delay: int) -> None:
		"""TEST:BB:DATA:RDELay \n
		No command help available \n
			:param restart_delay: No help available
		"""
		param = Conversions.decimal_value_to_str(restart_delay)
		self._core.io.write(f'TEST:BB:DATA:RDELay {param}')

	def get_state(self) -> bool:
		"""TEST:BB:DATA:STATe \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('TEST:BB:DATA:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""TEST:BB:DATA:STATe \n
		No command help available \n
			:param state: No help available
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'TEST:BB:DATA:STATe {param}')

	# noinspection PyTypeChecker
	def get_type_py(self) -> enums.BertTestMode:
		"""TEST:BB:DATA:TYPE \n
		Selects the type of error measurement. \n
			:return: type_py: BER| BLER
		"""
		response = self._core.io.query_str('TEST:BB:DATA:TYPE?')
		return Conversions.str_to_scalar_enum(response, enums.BertTestMode)

	def set_type_py(self, type_py: enums.BertTestMode) -> None:
		"""TEST:BB:DATA:TYPE \n
		Selects the type of error measurement. \n
			:param type_py: BER| BLER
		"""
		param = Conversions.enum_scalar_to_str(type_py, enums.BertTestMode)
		self._core.io.write(f'TEST:BB:DATA:TYPE {param}')
