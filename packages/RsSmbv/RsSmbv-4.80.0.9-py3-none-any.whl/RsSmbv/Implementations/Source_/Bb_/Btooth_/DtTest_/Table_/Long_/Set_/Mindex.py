from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mindex:
	"""Mindex commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mindex", core, parent)

	def set(self, mi_ndex: float, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:BTOoth:DTTest:TABLe:LONG:SET<CH>:MINDex \n
		Sets the modulation index, that specifies the frequency deviation. The modulation index h is defined as: with <img
		border='0' src='images/imga5f78ebf8bdb0adc0a00206a003a0641_1_--_--_PNG96.png' alt='' title=''>= 'symbol rate' , set with
		the command method RsSmbv.Source.Bb.Btooth.SymbolRate.
		variation <img border='0' src='images/img388349408bdb4b210a00206a01f5817c_1_--_--_PNG96.png' alt='' title=''>= 'frequency
		deviation', set with the command method RsSmbv.Source.Bb.Btooth.Msettings.fdeviation According to the Bluetooth standard,
		the modulation index is allowed to vary between 0.28 and 0.35. \n
			:param mi_ndex: float Range: 0.28 to 0.55
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Set')"""
		param = Conversions.decimal_value_to_str(mi_ndex)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:DTTest:TABLe:LONG:SET{channel_cmd_val}:MINDex {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""[SOURce<HW>]:BB:BTOoth:DTTest:TABLe:LONG:SET<CH>:MINDex \n
		Sets the modulation index, that specifies the frequency deviation. The modulation index h is defined as: with <img
		border='0' src='images/imga5f78ebf8bdb0adc0a00206a003a0641_1_--_--_PNG96.png' alt='' title=''>= 'symbol rate' , set with
		the command method RsSmbv.Source.Bb.Btooth.SymbolRate.
		variation <img border='0' src='images/img388349408bdb4b210a00206a01f5817c_1_--_--_PNG96.png' alt='' title=''>= 'frequency
		deviation', set with the command method RsSmbv.Source.Bb.Btooth.Msettings.fdeviation According to the Bluetooth standard,
		the modulation index is allowed to vary between 0.28 and 0.35. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Set')
			:return: mi_ndex: float Range: 0.28 to 0.55"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:BTOoth:DTTest:TABLe:LONG:SET{channel_cmd_val}:MINDex?')
		return Conversions.str_to_float(response)
