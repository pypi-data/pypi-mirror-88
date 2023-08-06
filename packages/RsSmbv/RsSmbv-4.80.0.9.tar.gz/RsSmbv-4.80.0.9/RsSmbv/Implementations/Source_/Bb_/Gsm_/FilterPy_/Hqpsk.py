from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Hqpsk:
	"""Hqpsk commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("hqpsk", core, parent)

	# noinspection PyTypeChecker
	def get_type_py(self) -> enums.GilterHigh:
		"""[SOURce<HW>]:BB:GSM:FILTer:HQPSk:TYPE \n
		Sets the filter for HSR QPSK signal. \n
			:return: type_py: ENPShape| EWPShape
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GSM:FILTer:HQPSk:TYPE?')
		return Conversions.str_to_scalar_enum(response, enums.GilterHigh)

	def set_type_py(self, type_py: enums.GilterHigh) -> None:
		"""[SOURce<HW>]:BB:GSM:FILTer:HQPSk:TYPE \n
		Sets the filter for HSR QPSK signal. \n
			:param type_py: ENPShape| EWPShape
		"""
		param = Conversions.enum_scalar_to_str(type_py, enums.GilterHigh)
		self._core.io.write(f'SOURce<HwInstance>:BB:GSM:FILTer:HQPSk:TYPE {param}')
