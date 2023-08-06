from typing import List

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Bstation:
	"""Bstation commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("bstation", core, parent)

	def get_catalog(self) -> List[str]:
		"""[SOURce<HW>]:BB:W3GPp:SETTing:TSETup:RECeiver:BSTation:CATalog \n
		No command help available \n
			:return: catalog: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:W3GPp:SETTing:TSETup:RECeiver:BSTation:CATalog?')
		return Conversions.str_to_str_list(response)

	def get_value(self) -> str:
		"""[SOURce<HW>]:BB:W3GPp:SETTing:TSETup:RECeiver:BSTation \n
		No command help available \n
			:return: bstation: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:W3GPp:SETTing:TSETup:RECeiver:BSTation?')
		return trim_str_response(response)

	def set_value(self, bstation: str) -> None:
		"""[SOURce<HW>]:BB:W3GPp:SETTing:TSETup:RECeiver:BSTation \n
		No command help available \n
			:param bstation: No help available
		"""
		param = Conversions.value_to_quoted_str(bstation)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:SETTing:TSETup:RECeiver:BSTation {param}')
