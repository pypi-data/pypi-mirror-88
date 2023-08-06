from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FilterPy:
	"""FilterPy commands group definition. 6 total commands, 0 Sub-groups, 6 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("filterPy", core, parent)

	# noinspection PyTypeChecker
	def get_bw(self) -> enums.FilterBandwidth:
		"""[SOURce<HW>]:BB:NR5G:SETTing:TMODel:FILTer:BW \n
		Applies a bandwidth filter to narrow down the files returned by the query method RsSmbv.Source.Bb.Nr5G.Setting.Tmodel.
		FilterPy.catalog. \n
			:return: filter_bandwidth: ALL| F5| F10| F15| F20| F25| F30| F40| F50| F60| F70| F80| F90| F100| F200| F400
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:SETTing:TMODel:FILTer:BW?')
		return Conversions.str_to_scalar_enum(response, enums.FilterBandwidth)

	def set_bw(self, filter_bandwidth: enums.FilterBandwidth) -> None:
		"""[SOURce<HW>]:BB:NR5G:SETTing:TMODel:FILTer:BW \n
		Applies a bandwidth filter to narrow down the files returned by the query method RsSmbv.Source.Bb.Nr5G.Setting.Tmodel.
		FilterPy.catalog. \n
			:param filter_bandwidth: ALL| F5| F10| F15| F20| F25| F30| F40| F50| F60| F70| F80| F90| F100| F200| F400
		"""
		param = Conversions.enum_scalar_to_str(filter_bandwidth, enums.FilterBandwidth)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:SETTing:TMODel:FILTer:BW {param}')

	def get_catalog(self) -> List[str]:
		"""[SOURce<HW>]:BB:NR5G:SETTing:TMODel:FILTer:CATalog \n
		Queries the filenames of predefined test signal files in the default directory after applying a filter. \n
			:return: nr_5_gcat_name_tmod_modified: filename1,filename2,... Returns a string of filenames separated by commas.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:SETTing:TMODel:FILTer:CATalog?')
		return Conversions.str_to_str_list(response)

	# noinspection PyTypeChecker
	def get_duplexing(self) -> enums.FilterDuplexing:
		"""[SOURce<HW>]:BB:NR5G:SETTing:TMODel:FILTer:DUPLexing \n
		Applies a duplexing filter to narrow down the files returned by the query method RsSmbv.Source.Bb.Nr5G.Setting.Tmodel.
		FilterPy.catalog. \n
			:return: filter_duplexing: ALL| FDD| TDD
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:SETTing:TMODel:FILTer:DUPLexing?')
		return Conversions.str_to_scalar_enum(response, enums.FilterDuplexing)

	def set_duplexing(self, filter_duplexing: enums.FilterDuplexing) -> None:
		"""[SOURce<HW>]:BB:NR5G:SETTing:TMODel:FILTer:DUPLexing \n
		Applies a duplexing filter to narrow down the files returned by the query method RsSmbv.Source.Bb.Nr5G.Setting.Tmodel.
		FilterPy.catalog. \n
			:param filter_duplexing: ALL| FDD| TDD
		"""
		param = Conversions.enum_scalar_to_str(filter_duplexing, enums.FilterDuplexing)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:SETTing:TMODel:FILTer:DUPLexing {param}')

	# noinspection PyTypeChecker
	def get_freq(self) -> enums.FilterFreqRange:
		"""[SOURce<HW>]:BB:NR5G:SETTing:TMODel:FILTer:FREQ \n
		Applies a frequency range filter to narrow down the files returned by the query method RsSmbv.Source.Bb.Nr5G.Setting.
		Tmodel.FilterPy.catalog. \n
			:return: filter_freq_range: ALL| FR1| FR2
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:SETTing:TMODel:FILTer:FREQ?')
		return Conversions.str_to_scalar_enum(response, enums.FilterFreqRange)

	def set_freq(self, filter_freq_range: enums.FilterFreqRange) -> None:
		"""[SOURce<HW>]:BB:NR5G:SETTing:TMODel:FILTer:FREQ \n
		Applies a frequency range filter to narrow down the files returned by the query method RsSmbv.Source.Bb.Nr5G.Setting.
		Tmodel.FilterPy.catalog. \n
			:param filter_freq_range: ALL| FR1| FR2
		"""
		param = Conversions.enum_scalar_to_str(filter_freq_range, enums.FilterFreqRange)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:SETTing:TMODel:FILTer:FREQ {param}')

	# noinspection PyTypeChecker
	def get_scs(self) -> enums.FilterSubcarrierSpacing:
		"""[SOURce<HW>]:BB:NR5G:SETTing:TMODel:FILTer:SCS \n
		Applies a subcarrier spacing filter to narrow down the files returned by the query method RsSmbv.Source.Bb.Nr5G.Setting.
		Tmodel.FilterPy.catalog. \n
			:return: filter_scs: ALL| F15| F30| F60| F120
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:SETTing:TMODel:FILTer:SCS?')
		return Conversions.str_to_scalar_enum(response, enums.FilterSubcarrierSpacing)

	def set_scs(self, filter_scs: enums.FilterSubcarrierSpacing) -> None:
		"""[SOURce<HW>]:BB:NR5G:SETTing:TMODel:FILTer:SCS \n
		Applies a subcarrier spacing filter to narrow down the files returned by the query method RsSmbv.Source.Bb.Nr5G.Setting.
		Tmodel.FilterPy.catalog. \n
			:param filter_scs: ALL| F15| F30| F60| F120
		"""
		param = Conversions.enum_scalar_to_str(filter_scs, enums.FilterSubcarrierSpacing)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:SETTing:TMODel:FILTer:SCS {param}')

	# noinspection PyTypeChecker
	def get_tmodel(self) -> enums.FilterTestModels:
		"""[SOURce<HW>]:BB:NR5G:SETTing:TMODel:FILTer:TMODel \n
		Applies a test model filter to narrow down the files returned by the query method RsSmbv.Source.Bb.Nr5G.Setting.Tmodel.
		FilterPy.catalog. \n
			:return: filter_test_model: ALL| TM1_1| TM1_2| TM2| TM2a| TM3_1| TM3_1A| TM3_2| TM3_3
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:SETTing:TMODel:FILTer:TMODel?')
		return Conversions.str_to_scalar_enum(response, enums.FilterTestModels)

	def set_tmodel(self, filter_test_model: enums.FilterTestModels) -> None:
		"""[SOURce<HW>]:BB:NR5G:SETTing:TMODel:FILTer:TMODel \n
		Applies a test model filter to narrow down the files returned by the query method RsSmbv.Source.Bb.Nr5G.Setting.Tmodel.
		FilterPy.catalog. \n
			:param filter_test_model: ALL| TM1_1| TM1_2| TM2| TM2a| TM3_1| TM3_1A| TM3_2| TM3_3
		"""
		param = Conversions.enum_scalar_to_str(filter_test_model, enums.FilterTestModels)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:SETTing:TMODel:FILTer:TMODel {param}')
