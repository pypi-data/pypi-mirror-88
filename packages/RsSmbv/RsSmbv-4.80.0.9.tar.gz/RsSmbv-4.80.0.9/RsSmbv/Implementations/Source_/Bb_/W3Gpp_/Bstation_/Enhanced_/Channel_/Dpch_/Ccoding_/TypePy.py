from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import enums
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TypePy:
	"""TypePy commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("typePy", core, parent)

	def set(self, type_py: enums.ChanCodType, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:BSTation:ENHanced:CHANnel<CH>:DPCH:CCODing:TYPE \n
		The command selects the channel coding scheme in accordance with the 3GPP specification. The 3GPP specification defines 4
		reference measurement channel coding types, which differ in the input data bit rate to be processed (12.2, 64, 144 and
		384 ksps) . The additional AMR CODER coding scheme generates the coding of a voice channel. The BTFD coding types with
		different data rates are also defined in the 3GPP specification (TS 34.121) . They are used for the receiver quality test
		Blind Transport Format Detection. When a channel coding type conforms to the standard and channel coding is activated,
		(method RsSmbv.Source.Bb.W3Gpp.Bstation.Enhanced.Channel.Dpch.Ccoding.State.set) the slot format (method RsSmbv.Source.Bb.
		W3Gpp.Bstation.Enhanced.Channel.Dpch.Ccoding.Sformat.set) and thus the symbol rate (method RsSmbv.Source.Bb.W3Gpp.
		Bstation.Enhanced.Channel.Dpch.Ccoding.SymbolRate.get_) , the bits per frame, (method RsSmbv.Source.Bb.W3Gpp.Bstation.
		Enhanced.Channel.Dpch.Ccoding.BpFrame.get_) , the pilot length (method RsSmbv.Source.Bb.W3Gpp.Bstation.Channel.Dpcch.
		Plength.set) and the TFCI state (method RsSmbv.Source.Bb.W3Gpp.Bstation.Channel.Dpcch.Tfci.State.set) are set to the
		associated values. \n
			:param type_py: M12K2| M64K| M144k| M384k| AMR| BTFD1| BTFD2| BTFD3 M12K2 Measurement channel with an input data bit rate of 12.2 ksps. M64K Measurement channel with an input data bit rate of 64 ksps. M144k Measurement channel with an input data bit rate of 144 ksps. M384k Measurement channel with an input data bit rate of 384 ksps. AMR Channel coding for the AMR Coder (coding a voice channel) . USER This parameter cannot be set. USER is returned whenever a user-defined channel coding is active, that is to say, after a channel coding parameter has been changed or a user coding file has been loaded. The file is loaded by the command method RsSmbv.Source.Bb.W3Gpp.Bstation.Enhanced.Channel.Dpch.Ccoding.User.load. BTFD1 Blind Transport Format Detection Rate 1 (12.2 kbps) . BTFD2 Blind Transport Format Detection Rate 2 (7.95 kbps) . BTFD3 Blind Transport Format Detection Rate 3 (1.95 kbps) .
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')"""
		param = Conversions.enum_scalar_to_str(type_py, enums.ChanCodType)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:BSTation:ENHanced:CHANnel{channel_cmd_val}:DPCH:CCODing:TYPE {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.ChanCodType:
		"""[SOURce<HW>]:BB:W3GPp:BSTation:ENHanced:CHANnel<CH>:DPCH:CCODing:TYPE \n
		The command selects the channel coding scheme in accordance with the 3GPP specification. The 3GPP specification defines 4
		reference measurement channel coding types, which differ in the input data bit rate to be processed (12.2, 64, 144 and
		384 ksps) . The additional AMR CODER coding scheme generates the coding of a voice channel. The BTFD coding types with
		different data rates are also defined in the 3GPP specification (TS 34.121) . They are used for the receiver quality test
		Blind Transport Format Detection. When a channel coding type conforms to the standard and channel coding is activated,
		(method RsSmbv.Source.Bb.W3Gpp.Bstation.Enhanced.Channel.Dpch.Ccoding.State.set) the slot format (method RsSmbv.Source.Bb.
		W3Gpp.Bstation.Enhanced.Channel.Dpch.Ccoding.Sformat.set) and thus the symbol rate (method RsSmbv.Source.Bb.W3Gpp.
		Bstation.Enhanced.Channel.Dpch.Ccoding.SymbolRate.get_) , the bits per frame, (method RsSmbv.Source.Bb.W3Gpp.Bstation.
		Enhanced.Channel.Dpch.Ccoding.BpFrame.get_) , the pilot length (method RsSmbv.Source.Bb.W3Gpp.Bstation.Channel.Dpcch.
		Plength.set) and the TFCI state (method RsSmbv.Source.Bb.W3Gpp.Bstation.Channel.Dpcch.Tfci.State.set) are set to the
		associated values. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')
			:return: type_py: M12K2| M64K| M144k| M384k| AMR| BTFD1| BTFD2| BTFD3 M12K2 Measurement channel with an input data bit rate of 12.2 ksps. M64K Measurement channel with an input data bit rate of 64 ksps. M144k Measurement channel with an input data bit rate of 144 ksps. M384k Measurement channel with an input data bit rate of 384 ksps. AMR Channel coding for the AMR Coder (coding a voice channel) . USER This parameter cannot be set. USER is returned whenever a user-defined channel coding is active, that is to say, after a channel coding parameter has been changed or a user coding file has been loaded. The file is loaded by the command method RsSmbv.Source.Bb.W3Gpp.Bstation.Enhanced.Channel.Dpch.Ccoding.User.load. BTFD1 Blind Transport Format Detection Rate 1 (12.2 kbps) . BTFD2 Blind Transport Format Detection Rate 2 (7.95 kbps) . BTFD3 Blind Transport Format Detection Rate 3 (1.95 kbps) ."""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:BSTation:ENHanced:CHANnel{channel_cmd_val}:DPCH:CCODing:TYPE?')
		return Conversions.str_to_scalar_enum(response, enums.ChanCodType)
