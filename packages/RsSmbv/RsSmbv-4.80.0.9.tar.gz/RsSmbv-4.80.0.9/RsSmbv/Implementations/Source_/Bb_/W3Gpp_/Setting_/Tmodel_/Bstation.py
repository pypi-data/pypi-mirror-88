from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Bstation:
	"""Bstation commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("bstation", core, parent)

	def get_catalog(self) -> List[str]:
		"""[SOURce<HW>]:BB:W3GPp:SETTing:TMODel:BSTation:CATalog \n
		Queries the list of test models defined by the standard for the downlink. \n
			:return: catalog: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:W3GPp:SETTing:TMODel:BSTation:CATalog?')
		return Conversions.str_to_str_list(response)

	def get_value(self) -> str:
		"""[SOURce<HW>]:BB:W3GPp:SETTing:TMODel:BSTation \n
		Selects a standard test model for the downlink. \n
			:return: bstation: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:W3GPp:SETTing:TMODel:BSTation?')
		return trim_str_response(response)

	def set_value(self, bstation: str) -> None:
		"""[SOURce<HW>]:BB:W3GPp:SETTing:TMODel:BSTation \n
		Selects a standard test model for the downlink. \n
			:param bstation: string
		"""
		param = Conversions.value_to_quoted_str(bstation)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:SETTing:TMODel:BSTation {param}')
