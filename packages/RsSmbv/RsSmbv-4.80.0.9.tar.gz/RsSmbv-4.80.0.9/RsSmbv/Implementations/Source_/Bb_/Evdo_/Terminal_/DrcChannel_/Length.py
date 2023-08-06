from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Length:
	"""Length commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("length", core, parent)

	def set(self, length: enums.EvdoDrcLenUp, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:EVDO:TERMinal<ST>:DRCChannel:LENGth \n
		(enabled for an access terminal working in traffic mode) Specifies the transmission duration of the Data Rate Control
		(DRC) channel in slots. \n
			:param length: DL1| DL2| DL4| DL8
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Terminal')"""
		param = Conversions.enum_scalar_to_str(length, enums.EvdoDrcLenUp)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EVDO:TERMinal{stream_cmd_val}:DRCChannel:LENGth {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.EvdoDrcLenUp:
		"""[SOURce<HW>]:BB:EVDO:TERMinal<ST>:DRCChannel:LENGth \n
		(enabled for an access terminal working in traffic mode) Specifies the transmission duration of the Data Rate Control
		(DRC) channel in slots. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Terminal')
			:return: length: DL1| DL2| DL4| DL8"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EVDO:TERMinal{stream_cmd_val}:DRCChannel:LENGth?')
		return Conversions.str_to_scalar_enum(response, enums.EvdoDrcLenUp)
