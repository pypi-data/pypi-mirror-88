from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class HrTimer:
	"""HrTimer commands group definition. 3 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("hrTimer", core, parent)

	def clone(self) -> 'HrTimer':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = HrTimer(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def absolute(self):
		"""absolute commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_absolute'):
			from .HrTimer_.Absolute import Absolute
			self._absolute = Absolute(self._core, self._base)
		return self._absolute

	def set_relative(self, pseudo_string: str) -> None:
		"""SYSTem:TIME:HRTimer:RELative \n
		No command help available \n
			:param pseudo_string: No help available
		"""
		param = Conversions.value_to_quoted_str(pseudo_string)
		self._core.io.write(f'SYSTem:TIME:HRTimer:RELative {param}')
