from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Emf:
	"""Emf commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("emf", core, parent)

	def get_state(self) -> bool:
		"""[SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:EMF:[STATe] \n
		Defines whether the EMF or the voltage value is used. \n
			:return: emf_state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:EMF:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, emf_state: bool) -> None:
		"""[SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:EMF:[STATe] \n
		Defines whether the EMF or the voltage value is used. \n
			:param emf_state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(emf_state)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:EMF:STATe {param}')
