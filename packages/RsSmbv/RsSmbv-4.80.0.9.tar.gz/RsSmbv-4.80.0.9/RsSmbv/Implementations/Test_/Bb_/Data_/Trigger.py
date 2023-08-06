from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Trigger:
	"""Trigger commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("trigger", core, parent)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.BertTgEnTrigMode:
		"""TEST:BB:DATA:TRIGger:[MODE] \n
		No command help available \n
			:return: trigger_mode: No help available
		"""
		response = self._core.io.query_str('TEST:BB:DATA:TRIGger:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.BertTgEnTrigMode)

	def set_mode(self, trigger_mode: enums.BertTgEnTrigMode) -> None:
		"""TEST:BB:DATA:TRIGger:[MODE] \n
		No command help available \n
			:param trigger_mode: No help available
		"""
		param = Conversions.enum_scalar_to_str(trigger_mode, enums.BertTgEnTrigMode)
		self._core.io.write(f'TEST:BB:DATA:TRIGger:MODE {param}')
