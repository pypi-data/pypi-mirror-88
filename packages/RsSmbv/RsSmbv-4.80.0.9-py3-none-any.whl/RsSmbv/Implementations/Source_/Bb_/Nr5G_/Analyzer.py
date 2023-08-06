from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Analyzer:
	"""Analyzer commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("analyzer", core, parent)

	def get_content(self) -> str:
		"""[SOURce<HW>]:BB:NR5G:ANALyzer:CONTent \n
		No command help available \n
			:return: export_xml: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:ANALyzer:CONTent?')
		return trim_str_response(response)

	def set_content(self, export_xml: str) -> None:
		"""[SOURce<HW>]:BB:NR5G:ANALyzer:CONTent \n
		No command help available \n
			:param export_xml: No help available
		"""
		param = Conversions.value_to_quoted_str(export_xml)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:ANALyzer:CONTent {param}')

	def get_create(self) -> List[str]:
		"""[SOURce<HW>]:BB:NR5G:ANALyzer:CREate \n
		No command help available \n
			:return: nr_5_gcat_name_export_xml: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:ANALyzer:CREate?')
		return Conversions.str_to_str_list(response)
