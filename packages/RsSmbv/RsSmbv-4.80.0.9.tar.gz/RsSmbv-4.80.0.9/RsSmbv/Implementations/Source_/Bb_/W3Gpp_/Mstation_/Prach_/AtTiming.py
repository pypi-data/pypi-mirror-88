from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AtTiming:
	"""AtTiming commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("atTiming", core, parent)

	def set(self, at_timing: enums.AichTranTim, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:PRACh:ATTiming \n
		This command defines which AICH Transmission Timing, time difference between the preamble and the message part or the
		time difference between two successive preambles in access slots, is defined. \n
			:param at_timing: ATT0| ATT1
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')"""
		param = Conversions.enum_scalar_to_str(at_timing, enums.AichTranTim)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:PRACh:ATTiming {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.AichTranTim:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:PRACh:ATTiming \n
		This command defines which AICH Transmission Timing, time difference between the preamble and the message part or the
		time difference between two successive preambles in access slots, is defined. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:return: at_timing: ATT0| ATT1"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:PRACh:ATTiming?')
		return Conversions.str_to_scalar_enum(response, enums.AichTranTim)
