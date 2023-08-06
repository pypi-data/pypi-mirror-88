from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Gain:
	"""Gain commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("gain", core, parent)

	def set(self, gain: float, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:EVDO:TERMinal<ST>:APCHannel:GAIN \n
		(enabled for Physical Layer subtype 2 and for an access terminal working in traffic mode) Sets the gain of the auxiliary
		pilot channel relative to the data channel power. Note: All other channel gains are specified relative to the pilot power,
		but the auxiliary pilot gain is specified relative to the data channel power. \n
			:param gain: float Range: -80 to 30
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Terminal')"""
		param = Conversions.decimal_value_to_str(gain)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EVDO:TERMinal{stream_cmd_val}:APCHannel:GAIN {param}')

	def get(self, stream=repcap.Stream.Default) -> float:
		"""[SOURce<HW>]:BB:EVDO:TERMinal<ST>:APCHannel:GAIN \n
		(enabled for Physical Layer subtype 2 and for an access terminal working in traffic mode) Sets the gain of the auxiliary
		pilot channel relative to the data channel power. Note: All other channel gains are specified relative to the pilot power,
		but the auxiliary pilot gain is specified relative to the data channel power. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Terminal')
			:return: gain: float Range: -80 to 30"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EVDO:TERMinal{stream_cmd_val}:APCHannel:GAIN?')
		return Conversions.str_to_float(response)
