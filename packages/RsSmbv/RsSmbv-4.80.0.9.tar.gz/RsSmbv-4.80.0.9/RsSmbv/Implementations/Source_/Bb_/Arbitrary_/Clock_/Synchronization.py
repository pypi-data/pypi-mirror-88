from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Synchronization:
	"""Synchronization commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("synchronization", core, parent)

	def clone(self) -> 'Synchronization':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Synchronization(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def execute(self):
		"""execute commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_execute'):
			from .Synchronization_.Execute import Execute
			self._execute = Execute(self._core, self._base)
		return self._execute

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.ClocSyncMode:
		"""[SOURce<HW>]:BB:ARBitrary:CLOCk:SYNChronization:MODE \n
		No command help available \n
			:return: mode: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:CLOCk:SYNChronization:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.ClocSyncMode)

	def set_mode(self, mode: enums.ClocSyncMode) -> None:
		"""[SOURce<HW>]:BB:ARBitrary:CLOCk:SYNChronization:MODE \n
		No command help available \n
			:param mode: No help available
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.ClocSyncMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:CLOCk:SYNChronization:MODE {param}')
