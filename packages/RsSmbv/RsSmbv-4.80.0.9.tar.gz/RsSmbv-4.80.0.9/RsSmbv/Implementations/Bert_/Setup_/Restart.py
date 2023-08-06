from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Restart:
	"""Restart commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("restart", core, parent)

	# noinspection PyTypeChecker
	def get_state(self) -> enums.BertRestState:
		"""BERT:SETup:RESTart:[STATe] \n
		Activates/deactivates an external restart of the BERT measurement. \n
			:return: state: 0| OFF| 1| ON
		"""
		response = self._core.io.query_str('BERT:SETup:RESTart:STATe?')
		return Conversions.str_to_scalar_enum(response, enums.BertRestState)

	def set_state(self, state: enums.BertRestState) -> None:
		"""BERT:SETup:RESTart:[STATe] \n
		Activates/deactivates an external restart of the BERT measurement. \n
			:param state: 0| OFF| 1| ON
		"""
		param = Conversions.enum_scalar_to_str(state, enums.BertRestState)
		self._core.io.write(f'BERT:SETup:RESTart:STATe {param}')
