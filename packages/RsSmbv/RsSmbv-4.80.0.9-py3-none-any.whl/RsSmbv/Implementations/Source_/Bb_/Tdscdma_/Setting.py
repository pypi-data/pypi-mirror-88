from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Setting:
	"""Setting commands group definition. 5 total commands, 1 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("setting", core, parent)

	def clone(self) -> 'Setting':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Setting(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def tmodel(self):
		"""tmodel commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_tmodel'):
			from .Setting_.Tmodel import Tmodel
			self._tmodel = Tmodel(self._core, self._base)
		return self._tmodel

	def get_catalog(self) -> List[str]:
		"""[SOURce<HW>]:BB:TDSCdma:SETTing:CATalog \n
		Queries the files with settings in the default directory. Listed are files with the file extension *.tdscdma. For general
		information on file handling in the default and in a specific directory, see section 'MMEMory Subsystem' in the R&S SMBVB
		user manual. \n
			:return: catalog: filename1,filename2,... Returns a string of filenames separated by commas.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:TDSCdma:SETTing:CATalog?')
		return Conversions.str_to_str_list(response)

	def load(self, filename: str) -> None:
		"""[SOURce<HW>]:BB:TDSCdma:SETTing:LOAD \n
		Loads the selected file from the default or the specified directory. Loaded are files with extension *.tdscdma. \n
			:param filename: 'filename' Filename or complete file path; file extension can be omitted
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:TDSCdma:SETTing:LOAD {param}')

	def set_store(self, filename: str) -> None:
		"""[SOURce<HW>]:BB:TDSCdma:SETTing:STORe \n
		Stores the current settings into the selected file; the file extension (*.tdscdma) is assigned automatically. \n
			:param filename: string Filename or complete file path
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:TDSCdma:SETTing:STORe {param}')
