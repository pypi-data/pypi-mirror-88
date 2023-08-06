from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Modulation:
	"""Modulation commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("modulation", core, parent)

	def set(self, modulation: enums.HsUpaMod, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:[HSUPa]:DPDCh:E:MODulation \n
		Sets the modulation of the E-DPDCH.
			INTRO_CMD_HELP: There are two possible modulation schemes specified for this channel, BPSK and 4PAM (4 Pulse-Amplitude Modulation) . The latter one is available only for the following Overall Symbol Rates (BB:W3GPp:DPDCh:E:ORATe) : \n
			- 2x960 ksps
			- 2x1920 ksps
			- 2x960 + 2x1920 ksps
			- 2x960 ksps, I or Q only
			- 2x1920 ksps, I or Q only
			- 2x960 + 2x1920 ksps, I or Q only \n
			:param modulation: BPSK| PAM4
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')"""
		param = Conversions.enum_scalar_to_str(modulation, enums.HsUpaMod)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:HSUPa:DPDCh:E:MODulation {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.HsUpaMod:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:[HSUPa]:DPDCh:E:MODulation \n
		Sets the modulation of the E-DPDCH.
			INTRO_CMD_HELP: There are two possible modulation schemes specified for this channel, BPSK and 4PAM (4 Pulse-Amplitude Modulation) . The latter one is available only for the following Overall Symbol Rates (BB:W3GPp:DPDCh:E:ORATe) : \n
			- 2x960 ksps
			- 2x1920 ksps
			- 2x960 + 2x1920 ksps
			- 2x960 ksps, I or Q only
			- 2x1920 ksps, I or Q only
			- 2x960 + 2x1920 ksps, I or Q only \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:return: modulation: BPSK| PAM4"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:HSUPa:DPDCh:E:MODulation?')
		return Conversions.str_to_scalar_enum(response, enums.HsUpaMod)
