from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class File:
	"""File commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("file", core, parent)

	def clone(self) -> 'File':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = File(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def tappend(self):
		"""tappend commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tappend'):
			from .File_.Tappend import Tappend
			self._tappend = Tappend(self._core, self._base)
		return self._tappend

	def get_directory(self) -> str:
		"""[SOURce<HW>]:BB:GNSS:LOGGing:DESTination:FILE:DIRectory \n
		Sets the storage place. \n
			:return: directory: string File path
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:LOGGing:DESTination:FILE:DIRectory?')
		return trim_str_response(response)

	def set_directory(self, directory: str) -> None:
		"""[SOURce<HW>]:BB:GNSS:LOGGing:DESTination:FILE:DIRectory \n
		Sets the storage place. \n
			:param directory: string File path
		"""
		param = Conversions.value_to_quoted_str(directory)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:LOGGing:DESTination:FILE:DIRectory {param}')
