from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Setting:
	"""Setting commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("setting", core, parent)

	def delete(self, filename: str) -> None:
		"""[SOURce<HW>]:ILS:SETTing:DELete \n
		Deletes the selected file from the default or the specified directory. Deleted are files with extension *.vor/*.ils/*.dme.
		Refer to 'Accessing Files in the Default or Specified Directory' for general information on file handling in the default
		and in a specific directory. \n
			:param filename: string
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:ILS:SETTing:DELete {param}')

	def load(self, filename: str) -> None:
		"""[SOURce<HW>]:ILS:SETTing:LOAD \n
		Loads the selected file from the default or the specified directory. Loaded are files with extension *.vor/*.ils/*.dme.
		Refer to 'Accessing Files in the Default or Specified Directory' for general information on file handling in the default
		and in a specific directory. \n
			:param filename: string
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:ILS:SETTing:LOAD {param}')

	def set_store(self, filename: str) -> None:
		"""[SOURce<HW>]:ILS:SETTing:STORe \n
		Saves the current settings into the selected file; the file extension (*.vor/*.ils/*.dme) is assigned automatically.
		Refer to 'Accessing Files in the Default or Specified Directory' for general information on file handling in the default
		and in a specific directory. \n
			:param filename: string
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:ILS:SETTing:STORe {param}')
