from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Prefix:
	"""Prefix commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("prefix", core, parent)

	def get_state(self) -> bool:
		"""HCOPy:FILE:[NAME]:AUTO:[FILE]:PREFix:STATe \n
		Uses the prefix for the automatic generation of the file name, provided PREF:STAT is activated. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('HCOPy:FILE:NAME:AUTO:FILE:PREFix:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""HCOPy:FILE:[NAME]:AUTO:[FILE]:PREFix:STATe \n
		Uses the prefix for the automatic generation of the file name, provided PREF:STAT is activated. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'HCOPy:FILE:NAME:AUTO:FILE:PREFix:STATe {param}')

	def get_value(self) -> str:
		"""HCOPy:FILE:[NAME]:AUTO:[FILE]:PREFix \n
		Uses the prefix for the automatic generation of the file name, provided PREF:STAT is activated. \n
			:return: prefix: No help available
		"""
		response = self._core.io.query_str('HCOPy:FILE:NAME:AUTO:FILE:PREFix?')
		return trim_str_response(response)

	def set_value(self, prefix: str) -> None:
		"""HCOPy:FILE:[NAME]:AUTO:[FILE]:PREFix \n
		Uses the prefix for the automatic generation of the file name, provided PREF:STAT is activated. \n
			:param prefix: 0| 1| OFF| ON
		"""
		param = Conversions.value_to_quoted_str(prefix)
		self._core.io.write(f'HCOPy:FILE:NAME:AUTO:FILE:PREFix {param}')
