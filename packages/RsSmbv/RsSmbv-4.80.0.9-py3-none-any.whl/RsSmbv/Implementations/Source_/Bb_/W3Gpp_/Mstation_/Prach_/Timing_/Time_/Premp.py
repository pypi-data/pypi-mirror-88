from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Premp:
	"""Premp commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("premp", core, parent)

	def set(self, premp: int, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:PRACh:TIMing:TIME:PREMp \n
		This command defines the AICH Transmission Timing. This parameter defines the time difference between the preamble and
		the message part. Two modes are defined in the standard. In mode 0, the preamble to message part difference is 3 access
		slots, in mode 1 it is 4 access slots. \n
			:param premp: integer Range: 1 to 14
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')"""
		param = Conversions.decimal_value_to_str(premp)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:PRACh:TIMing:TIME:PREMp {param}')

	def get(self, stream=repcap.Stream.Default) -> int:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:PRACh:TIMing:TIME:PREMp \n
		This command defines the AICH Transmission Timing. This parameter defines the time difference between the preamble and
		the message part. Two modes are defined in the standard. In mode 0, the preamble to message part difference is 3 access
		slots, in mode 1 it is 4 access slots. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:return: premp: integer Range: 1 to 14"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:PRACh:TIMing:TIME:PREMp?')
		return Conversions.str_to_int(response)
