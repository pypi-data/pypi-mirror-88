from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tdd:
	"""Tdd commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tdd", core, parent)

	def get_sps_conf(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:TDD:SPSConf \n
		In TDD mode, sets the special subframe configuration number. \n
			:return: spec_subfr_conf: integer Range: 0 to 9
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TDD:SPSConf?')
		return Conversions.str_to_int(response)

	def set_sps_conf(self, spec_subfr_conf: int) -> None:
		"""[SOURce<HW>]:BB:EUTRa:TDD:SPSConf \n
		In TDD mode, sets the special subframe configuration number. \n
			:param spec_subfr_conf: integer Range: 0 to 9
		"""
		param = Conversions.decimal_value_to_str(spec_subfr_conf)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:TDD:SPSConf {param}')

	def get_ud_conf(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:TDD:UDConf \n
		In TDD mode, sets the uplink/downlink configuration number. \n
			:return: uldl_conf: integer Range: 0 to 6
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TDD:UDConf?')
		return Conversions.str_to_int(response)

	def set_ud_conf(self, uldl_conf: int) -> None:
		"""[SOURce<HW>]:BB:EUTRa:TDD:UDConf \n
		In TDD mode, sets the uplink/downlink configuration number. \n
			:param uldl_conf: integer Range: 0 to 6
		"""
		param = Conversions.decimal_value_to_str(uldl_conf)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:TDD:UDConf {param}')

	# noinspection PyTypeChecker
	def get_upts(self) -> enums.Count:
		"""[SOURce<HW>]:BB:EUTRa:TDD:UPTS \n
		If method RsSmbv.Source.Bb.Eutra.Tdd.spsConf 10, sets the number of UpTPS symbols. \n
			:return: up_pts_symbol: 1| 2
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TDD:UPTS?')
		return Conversions.str_to_scalar_enum(response, enums.Count)

	def set_upts(self, up_pts_symbol: enums.Count) -> None:
		"""[SOURce<HW>]:BB:EUTRa:TDD:UPTS \n
		If method RsSmbv.Source.Bb.Eutra.Tdd.spsConf 10, sets the number of UpTPS symbols. \n
			:param up_pts_symbol: 1| 2
		"""
		param = Conversions.enum_scalar_to_str(up_pts_symbol, enums.Count)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:TDD:UPTS {param}')
