from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Cmns:
	"""Cmns commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cmns", core, parent)

	def get_pi(self) -> int:
		"""[SOURce<HW>]:BB:STEReo:GRPS:CMNS:PI \n
		No command help available \n
			:return: pi: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:STEReo:GRPS:CMNS:PI?')
		return Conversions.str_to_int(response)

	def set_pi(self, pi: int) -> None:
		"""[SOURce<HW>]:BB:STEReo:GRPS:CMNS:PI \n
		No command help available \n
			:param pi: No help available
		"""
		param = Conversions.decimal_value_to_str(pi)
		self._core.io.write(f'SOURce<HwInstance>:BB:STEReo:GRPS:CMNS:PI {param}')

	def get_pty(self) -> int:
		"""[SOURce<HW>]:BB:STEReo:GRPS:CMNS:PTY \n
		No command help available \n
			:return: pty: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:STEReo:GRPS:CMNS:PTY?')
		return Conversions.str_to_int(response)

	def set_pty(self, pty: int) -> None:
		"""[SOURce<HW>]:BB:STEReo:GRPS:CMNS:PTY \n
		No command help available \n
			:param pty: No help available
		"""
		param = Conversions.decimal_value_to_str(pty)
		self._core.io.write(f'SOURce<HwInstance>:BB:STEReo:GRPS:CMNS:PTY {param}')

	def get_tp(self) -> bool:
		"""[SOURce<HW>]:BB:STEReo:GRPS:CMNS:TP \n
		No command help available \n
			:return: tp: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:STEReo:GRPS:CMNS:TP?')
		return Conversions.str_to_bool(response)

	def set_tp(self, tp: bool) -> None:
		"""[SOURce<HW>]:BB:STEReo:GRPS:CMNS:TP \n
		No command help available \n
			:param tp: No help available
		"""
		param = Conversions.bool_to_str(tp)
		self._core.io.write(f'SOURce<HwInstance>:BB:STEReo:GRPS:CMNS:TP {param}')
