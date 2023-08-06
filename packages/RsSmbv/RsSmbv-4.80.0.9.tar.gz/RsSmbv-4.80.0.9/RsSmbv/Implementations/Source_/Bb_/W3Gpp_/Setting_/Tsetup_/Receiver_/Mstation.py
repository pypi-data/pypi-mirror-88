from typing import List

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mstation:
	"""Mstation commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mstation", core, parent)

	def get_catalog(self) -> List[str]:
		"""[SOURce<HW>]:BB:W3GPp:SETTing:TSETup:RECeiver:MSTation:CATalog \n
		No command help available \n
			:return: catalog: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:W3GPp:SETTing:TSETup:RECeiver:MSTation:CATalog?')
		return Conversions.str_to_str_list(response)

	def get_value(self) -> str:
		"""[SOURce<HW>]:BB:W3GPp:SETTing:TSETup:RECeiver:MSTation \n
		No command help available \n
			:return: mstation: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:W3GPp:SETTing:TSETup:RECeiver:MSTation?')
		return trim_str_response(response)

	def set_value(self, mstation: str) -> None:
		"""[SOURce<HW>]:BB:W3GPp:SETTing:TSETup:RECeiver:MSTation \n
		No command help available \n
			:param mstation: No help available
		"""
		param = Conversions.value_to_quoted_str(mstation)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:SETTing:TSETup:RECeiver:MSTation {param}')
