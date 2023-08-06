from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Copy:
	"""Copy commands group definition. 4 total commands, 1 Sub-groups, 3 group commands"""

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

	def get_coffset(self) -> int:
		"""[SOURce<HW>]:BB:W3GPp:COPY:COFFset \n
		Sets the offset for the channelization code in the destination base station. \n
			:return: co_ffset: integer Range: 0 to 511
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:W3GPp:COPY:COFFset?')
		return Conversions.str_to_int(response)

	def set_coffset(self, co_ffset: int) -> None:
		"""[SOURce<HW>]:BB:W3GPp:COPY:COFFset \n
		Sets the offset for the channelization code in the destination base station. \n
			:param co_ffset: integer Range: 0 to 511
		"""
		param = Conversions.decimal_value_to_str(co_ffset)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:COPY:COFFset {param}')

	# noinspection PyTypeChecker
	def get_destination(self) -> enums.NumberA:
		"""[SOURce<HW>]:BB:W3GPp:COPY:DESTination \n
		The command selects the station to which data is to be copied. Whether the data is copied to a base station or a user
		equipment depends on which transmission direction is selected (command W3GPp:LINK UP | DOWN) . \n
			:return: destination: 1| 2| 3| 4 Range: 1 to 4
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:W3GPp:COPY:DESTination?')
		return Conversions.str_to_scalar_enum(response, enums.NumberA)

	def set_destination(self, destination: enums.NumberA) -> None:
		"""[SOURce<HW>]:BB:W3GPp:COPY:DESTination \n
		The command selects the station to which data is to be copied. Whether the data is copied to a base station or a user
		equipment depends on which transmission direction is selected (command W3GPp:LINK UP | DOWN) . \n
			:param destination: 1| 2| 3| 4 Range: 1 to 4
		"""
		param = Conversions.enum_scalar_to_str(destination, enums.NumberA)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:COPY:DESTination {param}')

	# noinspection PyTypeChecker
	def get_source(self) -> enums.NumberA:
		"""[SOURce<HW>]:BB:W3GPp:COPY:SOURce \n
		The command selects the station that has data to be copied. Whether the station copied is a base or user equipment
		depends on which transmission direction is selected (command W3GPp:LINK UP | DOWN) . \n
			:return: source: 1| 2| 3| 4 Range: 1 to 4
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:W3GPp:COPY:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.NumberA)

	def set_source(self, source: enums.NumberA) -> None:
		"""[SOURce<HW>]:BB:W3GPp:COPY:SOURce \n
		The command selects the station that has data to be copied. Whether the station copied is a base or user equipment
		depends on which transmission direction is selected (command W3GPp:LINK UP | DOWN) . \n
			:param source: 1| 2| 3| 4 Range: 1 to 4
		"""
		param = Conversions.enum_scalar_to_str(source, enums.NumberA)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:COPY:SOURce {param}')
