from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dwell:
	"""Dwell commands group definition. 4 total commands, 1 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dwell", core, parent)

	def clone(self) -> 'Dwell':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Dwell(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def listPy(self):
		"""listPy commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_listPy'):
			from .Dwell_.ListPy import ListPy
			self._listPy = ListPy(self._core, self._base)
		return self._listPy

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.ParameterSetMode:
		"""[SOURce<HW>]:LIST:DWELl:MODE \n
		Selects the dwell time mode. \n
			:return: dwel_mode: LIST| GLOBal LIST Uses the dwell time, specified in the data table for each value pair individually. GLOBal Uses a constant dwell time, set with command method RsSmbv.Source.ListPy.Dwell.value.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:LIST:DWELl:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.ParameterSetMode)

	def set_mode(self, dwel_mode: enums.ParameterSetMode) -> None:
		"""[SOURce<HW>]:LIST:DWELl:MODE \n
		Selects the dwell time mode. \n
			:param dwel_mode: LIST| GLOBal LIST Uses the dwell time, specified in the data table for each value pair individually. GLOBal Uses a constant dwell time, set with command method RsSmbv.Source.ListPy.Dwell.value.
		"""
		param = Conversions.enum_scalar_to_str(dwel_mode, enums.ParameterSetMode)
		self._core.io.write(f'SOURce<HwInstance>:LIST:DWELl:MODE {param}')

	def get_value(self) -> float:
		"""[SOURce<HW>]:LIST:DWELl \n
		Sets the global dwell time. The instrument generates the signal with the frequency / power value pairs of ​​each list
		entry for that particular period. See also 'Significant Parameters and Functions'. \n
			:return: dwell: float Range: 1E-3 to 100
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:LIST:DWELl?')
		return Conversions.str_to_float(response)

	def set_value(self, dwell: float) -> None:
		"""[SOURce<HW>]:LIST:DWELl \n
		Sets the global dwell time. The instrument generates the signal with the frequency / power value pairs of ​​each list
		entry for that particular period. See also 'Significant Parameters and Functions'. \n
			:param dwell: float Range: 1E-3 to 100
		"""
		param = Conversions.decimal_value_to_str(dwell)
		self._core.io.write(f'SOURce<HwInstance>:LIST:DWELl {param}')
