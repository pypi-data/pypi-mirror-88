from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Setting:
	"""Setting commands group definition. 16 total commands, 2 Sub-groups, 4 group commands"""

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
		"""tmodel commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_tmodel'):
			from .Setting_.Tmodel import Tmodel
			self._tmodel = Tmodel(self._core, self._base)
		return self._tmodel

	@property
	def tsetup(self):
		"""tsetup commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_tsetup'):
			from .Setting_.Tsetup import Tsetup
			self._tsetup = Tsetup(self._core, self._base)
		return self._tsetup

	def get_catalog(self) -> List[str]:
		"""[SOURce<HW>]:BB:W3GPp:SETTing:CATalog \n
		This command reads out the files with 3GPP FDD settings in the default directory. The default directory is set using
		command method RsSmbv.MassMemory.currentDirectory. Only files with the file extension *.3g are listed. \n
			:return: catalog: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:W3GPp:SETTing:CATalog?')
		return Conversions.str_to_str_list(response)

	def delete(self, filename: str) -> None:
		"""[SOURce<HW>]:BB:W3GPp:SETTing:DELete \n
		This command deletes the selected file with 3GPP FDD settings. The directory is set using command method RsSmbv.
		MassMemory.currentDirectory. A path can also be specified, in which case the files in the specified directory are read.
		The file extension can be omitted. Only files with the file extension *.3g are deleted. \n
			:param filename: file_name
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:SETTing:DELete {param}')

	def load(self, filename: str) -> None:
		"""[SOURce<HW>]:BB:W3GPp:SETTing:LOAD \n
		This command loads the selected file with 3GPP FDD settings. The directory is set using command method RsSmbv.MassMemory.
		currentDirectory. A path can also be specified, in which case the files in the specified directory are read. The file
		extension can be omitted. Only files with the file extension *.3g are loaded. \n
			:param filename: file_name
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:SETTing:LOAD {param}')

	def set_store(self, filename: str) -> None:
		"""[SOURce<HW>]:BB:W3GPp:SETTing:STORe \n
		This command stores the current 3GPP FDD settings into the selected file. The directory is set using command method
		RsSmbv.MassMemory.currentDirectory. A path can also be specified, in which case the files in the specified directory are
		read. Only enter the file name. 3GPP FDD settings are stored as files with the specific file extensions *.3g. \n
			:param filename: string
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:SETTing:STORe {param}')
