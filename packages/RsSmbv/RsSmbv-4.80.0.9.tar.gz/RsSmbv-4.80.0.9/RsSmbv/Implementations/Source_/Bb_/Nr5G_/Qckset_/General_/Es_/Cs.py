from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Cs:
	"""Cs commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cs", core, parent)

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:NR5G:QCKSet:GENeral:ES:CS:STATe \n
		Activate to schedule a CORESET. \n
			:return: qck_set_cs_state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:QCKSet:GENeral:ES:CS:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, qck_set_cs_state: bool) -> None:
		"""[SOURce<HW>]:BB:NR5G:QCKSet:GENeral:ES:CS:STATe \n
		Activate to schedule a CORESET. \n
			:param qck_set_cs_state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(qck_set_cs_state)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:QCKSet:GENeral:ES:CS:STATe {param}')
