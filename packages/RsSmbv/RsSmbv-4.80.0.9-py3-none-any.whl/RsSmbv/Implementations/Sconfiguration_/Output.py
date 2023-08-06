from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Output:
	"""Output commands group definition. 9 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("output", core, parent)

	def clone(self) -> 'Output':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Output(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def mapping(self):
		"""mapping commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_mapping'):
			from .Output_.Mapping import Mapping
			self._mapping = Mapping(self._core, self._base)
		return self._mapping

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.SystConfOutpMode:
		"""SCONfiguration:OUTPut:MODE \n
		No command help available \n
			:return: mode: No help available
		"""
		response = self._core.io.query_str('SCONfiguration:OUTPut:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.SystConfOutpMode)

	def set_mode(self, mode: enums.SystConfOutpMode) -> None:
		"""SCONfiguration:OUTPut:MODE \n
		No command help available \n
			:param mode: No help available
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.SystConfOutpMode)
		self._core.io.write(f'SCONfiguration:OUTPut:MODE {param}')
