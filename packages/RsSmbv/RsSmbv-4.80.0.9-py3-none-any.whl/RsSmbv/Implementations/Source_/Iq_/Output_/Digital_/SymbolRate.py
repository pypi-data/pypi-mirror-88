from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SymbolRate:
	"""SymbolRate commands group definition. 6 total commands, 2 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("symbolRate", core, parent)

	def clone(self) -> 'SymbolRate':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SymbolRate(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def common(self):
		"""common commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_common'):
			from .SymbolRate_.Common import Common
			self._common = Common(self._core, self._base)
		return self._common

	@property
	def fifo(self):
		"""fifo commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fifo'):
			from .SymbolRate_.Fifo import Fifo
			self._fifo = Fifo(self._core, self._base)
		return self._fifo

	def get_max(self) -> int:
		"""[SOURce]:IQ:OUTPut:DIGital:SRATe:MAX \n
		Queries the maximum supported sample rate. \n
			:return: dig_iqhs_in_sr_max: integer Range: 400 to 600E6
		"""
		response = self._core.io.query_str('SOURce:IQ:OUTPut:DIGital:SRATe:MAX?')
		return Conversions.str_to_int(response)

	# noinspection PyTypeChecker
	def get_source(self) -> enums.BboutClocSour:
		"""[SOURce<HW>]:IQ:OUTPut:DIGital:SRATe:SOURce \n
		Selects whether the sample rate is estimated based on the digital signal or is a user-defined value. \n
			:return: source: USER| DOUT
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:DIGital:SRATe:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.BboutClocSour)

	def set_source(self, source: enums.BboutClocSour) -> None:
		"""[SOURce<HW>]:IQ:OUTPut:DIGital:SRATe:SOURce \n
		Selects whether the sample rate is estimated based on the digital signal or is a user-defined value. \n
			:param source: USER| DOUT
		"""
		param = Conversions.enum_scalar_to_str(source, enums.BboutClocSour)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:DIGital:SRATe:SOURce {param}')

	def get_sum(self) -> int:
		"""[SOURce]:IQ:OUTPut:DIGital:SRATe:SUM \n
		Queries the maximum supported sample rate. \n
			:return: dig_iqhs_in_sr_sum: integer Range: 400 to 600E6
		"""
		response = self._core.io.query_str('SOURce:IQ:OUTPut:DIGital:SRATe:SUM?')
		return Conversions.str_to_int(response)

	def get_value(self) -> float:
		"""[SOURce<HW>]:IQ:OUTPut:DIGital:SRATe \n
		Sets/queries the sample rate of the digital I/Q output signal. \n
			:return: srate: float Range: 400 to max* *) max value depends on the interface as follows: If 'Interface = Dig. I/Q', max = 250E6 and depends on connected receiving device If 'Interface = HS Dig. I/Q', max = 600E6
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:DIGital:SRATe?')
		return Conversions.str_to_float(response)

	def set_value(self, srate: float) -> None:
		"""[SOURce<HW>]:IQ:OUTPut:DIGital:SRATe \n
		Sets/queries the sample rate of the digital I/Q output signal. \n
			:param srate: float Range: 400 to max* *) max value depends on the interface as follows: If 'Interface = Dig. I/Q', max = 250E6 and depends on connected receiving device If 'Interface = HS Dig. I/Q', max = 600E6
		"""
		param = Conversions.decimal_value_to_str(srate)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:DIGital:SRATe {param}')
