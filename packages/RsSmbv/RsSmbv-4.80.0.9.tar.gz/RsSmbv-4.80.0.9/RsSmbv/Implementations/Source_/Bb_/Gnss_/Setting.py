from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Setting:
	"""Setting commands group definition. 6 total commands, 2 Sub-groups, 3 group commands"""

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
	def catalog(self):
		"""catalog commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_catalog'):
			from .Setting_.Catalog import Catalog
			self._catalog = Catalog(self._core, self._base)
		return self._catalog

	@property
	def load(self):
		"""load commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_load'):
			from .Setting_.Load import Load
			self._load = Load(self._core, self._base)
		return self._load

	def delete(self, filename: str) -> None:
		"""[SOURce<HW>]:BB:GNSS:SETTing:DELete \n
		Deletes the selected file from the default or the specified directory. Refer to 'Accessing Files in the Default or
		Specified Directory' for general information on file handling in the default and in a specific directory. \n
			:param filename: 'filename' Filename or complete file path; file extension can be omitted
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SETTing:DELete {param}')

	def load_file(self, filename: str) -> None:
		"""[SOURce<HW>]:BB:GNSS:SETTing:LOAD \n
		Loads the selected file from the default or the specified directory. Loaded are files with extension *.gnss. Refer to
		'Accessing Files in the Default or Specified Directory' for general information on file handling in the default and in a
		specific directory. \n
			:param filename: 'filename' Filename or complete file path; file extension can be omitted Query the existing files with the command method RsSmbv.Source.Bb.Gnss.Setting.Catalog.value.
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SETTing:LOAD {param}')

	def set_store(self, filename: str) -> None:
		"""[SOURce<HW>]:BB:GNSS:SETTing:STORe \n
		Saves the current settings into the selected file; the file extension (*.gnss) is assigned automatically.
		Refer to 'Accessing Files in the Default or Specified Directory' for general information on file handling in the default
		and in a specific directory. \n
			:param filename: 'filename' Filename or complete file path
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SETTing:STORe {param}')
