from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mod:
	"""Mod commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mod", core, parent)

	def set(self, mode: enums.IdEutraNbiotMode, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:UE<ST>:PRACh:NIOT:MOD \n
		Selects the operating mode. \n
			:param mode: INBD| ALON| GBD
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')"""
		param = Conversions.enum_scalar_to_str(mode, enums.IdEutraNbiotMode)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:PRACh:NIOT:MOD {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.IdEutraNbiotMode:
		"""[SOURce<HW>]:BB:EUTRa:UL:UE<ST>:PRACh:NIOT:MOD \n
		Selects the operating mode. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:return: mode: INBD| ALON| GBD"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:PRACh:NIOT:MOD?')
		return Conversions.str_to_scalar_enum(response, enums.IdEutraNbiotMode)
