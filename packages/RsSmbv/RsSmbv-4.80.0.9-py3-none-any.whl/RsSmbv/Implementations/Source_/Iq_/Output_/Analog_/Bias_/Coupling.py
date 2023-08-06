from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Coupling:
	"""Coupling commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("coupling", core, parent)

	def get_state(self) -> bool:
		"""[SOURce<HW>]:IQ:OUTPut:[ANALog]:BIAS:COUPling:[STATe] \n
		Couples the bias setting of the I and Q signal components. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:ANALog:BIAS:COUPling:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce<HW>]:IQ:OUTPut:[ANALog]:BIAS:COUPling:[STATe] \n
		Couples the bias setting of the I and Q signal components. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:BIAS:COUPling:STATe {param}')
