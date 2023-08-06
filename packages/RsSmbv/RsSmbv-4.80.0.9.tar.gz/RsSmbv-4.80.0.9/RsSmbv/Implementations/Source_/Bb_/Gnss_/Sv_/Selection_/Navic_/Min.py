from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Min:
	"""Min commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("min", core, parent)

	def set(self, minimum_sv_s: int, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:SV:SELection:NAVic<ST>:MIN \n
		Sets the minimum and maximum number of satellites per GNSS system that can be included in the satellite constellation. \n
			:param minimum_sv_s: integer Range: 0 to 24
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Navic')"""
		param = Conversions.decimal_value_to_str(minimum_sv_s)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SV:SELection:NAVic{stream_cmd_val}:MIN {param}')

	def get(self, stream=repcap.Stream.Default) -> int:
		"""[SOURce<HW>]:BB:GNSS:SV:SELection:NAVic<ST>:MIN \n
		Sets the minimum and maximum number of satellites per GNSS system that can be included in the satellite constellation. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Navic')
			:return: minimum_sv_s: No help available"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SV:SELection:NAVic{stream_cmd_val}:MIN?')
		return Conversions.str_to_int(response)
