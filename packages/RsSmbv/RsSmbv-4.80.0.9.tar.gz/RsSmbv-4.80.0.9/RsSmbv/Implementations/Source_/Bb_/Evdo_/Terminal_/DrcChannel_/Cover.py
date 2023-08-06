from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Cover:
	"""Cover commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cover", core, parent)

	def set(self, cover: int, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:EVDO:TERMinal<ST>:DRCChannel:COVer \n
		(enabled for an access terminal working in traffic mode) Selects the Data Rate Control (DRC) Channel Walsh cover. \n
			:param cover: integer Range: 0 to 7
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Terminal')"""
		param = Conversions.decimal_value_to_str(cover)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EVDO:TERMinal{stream_cmd_val}:DRCChannel:COVer {param}')

	def get(self, stream=repcap.Stream.Default) -> int:
		"""[SOURce<HW>]:BB:EVDO:TERMinal<ST>:DRCChannel:COVer \n
		(enabled for an access terminal working in traffic mode) Selects the Data Rate Control (DRC) Channel Walsh cover. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Terminal')
			:return: cover: integer Range: 0 to 7"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EVDO:TERMinal{stream_cmd_val}:DRCChannel:COVer?')
		return Conversions.str_to_int(response)
