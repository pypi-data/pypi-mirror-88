from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pmode:
	"""Pmode commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pmode", core, parent)

	def set(self, power_mode: enums.EutraPhichPwrMode, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:[SUBF<ST>]:ENCC:PHICh:PMODe \n
		Determines whether the PHICHs in a PHICH group are sent with the same power or enables the adjustment of each PPHICH
		individually. \n
			:param power_mode: CONSt| IND CONSt The power of a PHICH in a PHICH group is set with the command SOUR:BB:EUTR:DL:ENCC:PHIC:POW. IND The power of the individual PHICHs is set separatelly
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')"""
		param = Conversions.enum_scalar_to_str(power_mode, enums.EutraPhichPwrMode)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:SUBF{stream_cmd_val}:ENCC:PHICh:PMODe {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.EutraPhichPwrMode:
		"""[SOURce<HW>]:BB:EUTRa:DL:[SUBF<ST>]:ENCC:PHICh:PMODe \n
		Determines whether the PHICHs in a PHICH group are sent with the same power or enables the adjustment of each PPHICH
		individually. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:return: power_mode: CONSt| IND CONSt The power of a PHICH in a PHICH group is set with the command SOUR:BB:EUTR:DL:ENCC:PHIC:POW. IND The power of the individual PHICHs is set separatelly"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:SUBF{stream_cmd_val}:ENCC:PHICh:PMODe?')
		return Conversions.str_to_scalar_enum(response, enums.EutraPhichPwrMode)
