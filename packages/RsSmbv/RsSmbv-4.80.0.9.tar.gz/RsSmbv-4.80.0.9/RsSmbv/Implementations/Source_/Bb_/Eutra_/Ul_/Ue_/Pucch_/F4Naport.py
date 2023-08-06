from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class F4Naport:
	"""F4Naport commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("f4Naport", core, parent)

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.EutraPucchNumAp:
		"""[SOURce<HW>]:BB:EUTRa:UL:UE<ST>:PUCCh:F4Naport \n
		For LTE-A UEs, sets the number of antenna ports used for every PUCCH format transmission. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:return: pucch_f_4_num_aps: No help available"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:PUCCh:F4Naport?')
		return Conversions.str_to_scalar_enum(response, enums.EutraPucchNumAp)
