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
	def get_sequence(self) -> enums.DmTrigMode:
		"""[SOURce<HW>]:BB:GNPR:[TRIGger]:SEQuence \n
		No command help available \n
			:return: sequence: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNPR:TRIGger:SEQuence?')
		return Conversions.str_to_scalar_enum(response, enums.DmTrigMode)

	def set_sequence(self, sequence: enums.DmTrigMode) -> None:
		"""[SOURce<HW>]:BB:GNPR:[TRIGger]:SEQuence \n
		No command help available \n
			:param sequence: No help available
		"""
		param = Conversions.enum_scalar_to_str(sequence, enums.DmTrigMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNPR:TRIGger:SEQuence {param}')
