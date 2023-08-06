from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Power:
	"""Power commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("power", core, parent)

	def get_att_digital(self) -> float:
		"""[SOURce<HW>]:IQ:OUTPut:[ANALog]:POWer:ATTDigital \n
		For IQ:MODEVATTenuated, set the attenution with that the signal is attenuated. \n
			:return: dattenuation: float Range: -3.522 to 80
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:ANALog:POWer:ATTDigital?')
		return Conversions.str_to_float(response)

	def set_att_digital(self, dattenuation: float) -> None:
		"""[SOURce<HW>]:IQ:OUTPut:[ANALog]:POWer:ATTDigital \n
		For IQ:MODEVATTenuated, set the attenution with that the signal is attenuated. \n
			:param dattenuation: float Range: -3.522 to 80
		"""
		param = Conversions.decimal_value_to_str(dattenuation)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:POWer:ATTDigital {param}')
