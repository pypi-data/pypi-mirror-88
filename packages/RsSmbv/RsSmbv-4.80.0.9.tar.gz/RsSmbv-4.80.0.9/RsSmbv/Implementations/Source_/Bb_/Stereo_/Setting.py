from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Setting:
	"""Setting commands group definition. 4 total commands, 1 Sub-groups, 2 group commands"""

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
	def store(self):
		"""store commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_store'):
			from .Setting_.Store import Store
			self._store = Store(self._core, self._base)
		return self._store

	def get_catalog(self) -> List[str]:
		"""[SOURce<HW>]:BB:STEReo:SETTing:CATalog \n
		No command help available \n
			:return: catalog: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:STEReo:SETTing:CATalog?')
		return Conversions.str_to_str_list(response)

	def load(self, load: str) -> None:
		"""[SOURce<HW>]:BB:STEReo:SETTing:LOAD \n
		No command help available \n
			:param load: No help available
		"""
		param = Conversions.value_to_quoted_str(load)
		self._core.io.write(f'SOURce<HwInstance>:BB:STEReo:SETTing:LOAD {param}')
