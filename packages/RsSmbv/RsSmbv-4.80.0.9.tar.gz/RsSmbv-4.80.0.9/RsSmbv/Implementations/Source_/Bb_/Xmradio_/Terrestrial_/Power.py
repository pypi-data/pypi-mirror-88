from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Power:
	"""Power commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("power", core, parent)

	def get_amss(self) -> float:
		"""[SOURce<HW>]:BB:XMRadio:TERRestrial:POWer:AMSS \n
		No command help available \n
			:return: amss: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:XMRadio:TERRestrial:POWer:AMSS?')
		return Conversions.str_to_float(response)

	def set_amss(self, amss: float) -> None:
		"""[SOURce<HW>]:BB:XMRadio:TERRestrial:POWer:AMSS \n
		No command help available \n
			:param amss: No help available
		"""
		param = Conversions.decimal_value_to_str(amss)
		self._core.io.write(f'SOURce<HwInstance>:BB:XMRadio:TERRestrial:POWer:AMSS {param}')

	def get_mcm(self) -> float:
		"""[SOURce<HW>]:BB:XMRadio:TERRestrial:POWer:MCM \n
		No command help available \n
			:return: mcm: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:XMRadio:TERRestrial:POWer:MCM?')
		return Conversions.str_to_float(response)

	def set_mcm(self, mcm: float) -> None:
		"""[SOURce<HW>]:BB:XMRadio:TERRestrial:POWer:MCM \n
		No command help available \n
			:param mcm: No help available
		"""
		param = Conversions.decimal_value_to_str(mcm)
		self._core.io.write(f'SOURce<HwInstance>:BB:XMRadio:TERRestrial:POWer:MCM {param}')
