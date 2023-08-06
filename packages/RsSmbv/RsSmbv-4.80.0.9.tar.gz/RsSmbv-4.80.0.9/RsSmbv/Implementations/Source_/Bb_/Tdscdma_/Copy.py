from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Copy:
	"""Copy commands group definition. 3 total commands, 1 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("copy", core, parent)

	def clone(self) -> 'Copy':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Copy(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def execute(self):
		"""execute commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_execute'):
			from .Copy_.Execute import Execute
			self._execute = Execute(self._core, self._base)
		return self._execute

	# noinspection PyTypeChecker
	def get_destination(self) -> enums.NumberA:
		"""[SOURce<HW>]:BB:TDSCdma:COPY:DESTination \n
		Selects the cell whose settings are to be overwritten. \n
			:return: destination: 1| 2| 3| 4 Range: 1 to 4
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:TDSCdma:COPY:DESTination?')
		return Conversions.str_to_scalar_enum(response, enums.NumberA)

	def set_destination(self, destination: enums.NumberA) -> None:
		"""[SOURce<HW>]:BB:TDSCdma:COPY:DESTination \n
		Selects the cell whose settings are to be overwritten. \n
			:param destination: 1| 2| 3| 4 Range: 1 to 4
		"""
		param = Conversions.enum_scalar_to_str(destination, enums.NumberA)
		self._core.io.write(f'SOURce<HwInstance>:BB:TDSCdma:COPY:DESTination {param}')

	# noinspection PyTypeChecker
	def get_source(self) -> enums.NumberA:
		"""[SOURce<HW>]:BB:TDSCdma:COPY:SOURce \n
		Selects the cell whose settings are to be copied. \n
			:return: source: 1| 2| 3| 4 Range: 1 to 4
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:TDSCdma:COPY:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.NumberA)

	def set_source(self, source: enums.NumberA) -> None:
		"""[SOURce<HW>]:BB:TDSCdma:COPY:SOURce \n
		Selects the cell whose settings are to be copied. \n
			:param source: 1| 2| 3| 4 Range: 1 to 4
		"""
		param = Conversions.enum_scalar_to_str(source, enums.NumberA)
		self._core.io.write(f'SOURce<HwInstance>:BB:TDSCdma:COPY:SOURce {param}')
