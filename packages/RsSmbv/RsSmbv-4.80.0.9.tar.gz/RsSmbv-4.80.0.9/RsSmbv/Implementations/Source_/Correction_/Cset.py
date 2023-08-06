from typing import List

from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Cset:
	"""Cset commands group definition. 8 total commands, 1 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cset", core, parent)

	def clone(self) -> 'Cset':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Cset(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def data(self):
		"""data commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_data'):
			from .Cset_.Data import Data
			self._data = Data(self._core, self._base)
		return self._data

	def get_catalog(self) -> List[str]:
		"""[SOURce]:CORRection:CSET:CATalog \n
		Queries a list of available user correction tables. \n
			:return: catalog: string List of list filenames, separated by commas
		"""
		response = self._core.io.query_str('SOURce:CORRection:CSET:CATalog?')
		return Conversions.str_to_str_list(response)

	def delete(self, filename: str) -> None:
		"""[SOURce]:CORRection:CSET:DELete \n
		Deletes the specified user correction list file. \n
			:param filename: string Filename or complete file path; file extension is optional.
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce:CORRection:CSET:DELete {param}')

	def get_select(self) -> str:
		"""[SOURce<HW>]:CORRection:CSET:[SELect] \n
		Selects or creates a file for the user correction data. If the file with the selected name does not exist, a new file is
		created. \n
			:return: filename: string Filename or complete file path; file extension can be omitted.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:CORRection:CSET:SELect?')
		return trim_str_response(response)

	def set_select(self, filename: str) -> None:
		"""[SOURce<HW>]:CORRection:CSET:[SELect] \n
		Selects or creates a file for the user correction data. If the file with the selected name does not exist, a new file is
		created. \n
			:param filename: string Filename or complete file path; file extension can be omitted.
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:CORRection:CSET:SELect {param}')
