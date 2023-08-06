from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class F2Naport:
	"""F2Naport commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("f2Naport", core, parent)

	def set(self, num_aps: enums.EutraPucchNumAp, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:UE<ST>:PUCCh:F2Naport \n
		For LTE-A UEs, sets the number of antenna ports used for every PUCCH format transmission. \n
			:param num_aps: AP1| AP2
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')"""
		param = Conversions.enum_scalar_to_str(num_aps, enums.EutraPucchNumAp)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:PUCCh:F2Naport {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.EutraPucchNumAp:
		"""[SOURce<HW>]:BB:EUTRa:UL:UE<ST>:PUCCh:F2Naport \n
		For LTE-A UEs, sets the number of antenna ports used for every PUCCH format transmission. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:return: num_aps: AP1| AP2"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:PUCCh:F2Naport?')
		return Conversions.str_to_scalar_enum(response, enums.EutraPucchNumAp)
