from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sformat:
	"""Sformat commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sformat", core, parent)

	def set(self, sf_ormat: int, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:BSTation:ENHanced:CHANnel<CH>:DPCH:CCODing:SFORmat \n
		The command sets the slot format for the selected enhanced DPCH of base station 1. The slot format is fixed for
		channel-coded measurement channels conforming to the standard - 'Reference Measurement Channel'. Changing the slot format
		automatically activates User coding (W3GP:BST:ENH:CHAN<11...13>:DPCH:CCOD:TYPE USER) . The slot format also fixes the
		symbol rate, bits per frame, pilot length and TFCI state parameters. When a channel coding type conforming to the
		standard is selected (method RsSmbv.Source.Bb.W3Gpp.Bstation.Enhanced.Channel.Dpch.Ccoding.TypePy.set) and channel coding
		is activated, the slot format is (method RsSmbv.Source.Bb.W3Gpp.Bstation.Enhanced.Channel.Dpch.Ccoding.State.
		set) automatically set to the associated value. Changing the slot format automatically activates User coding
		(W3GP:BST:ENH:CHAN<11...13>:DPCH:CCOD:TYPE USER) . The command sets the symbol rate (W3GP:BST:ENH:CHAN:DPCH:CCOD:SRAT) ,
		the bits per frame (W3GP:BST:ENH:CHAN:DPCH:CCOD:BPFR) , the pilot length (W3GP:BST1:CHAN:DPCC:PLEN) , and the TFCI state
		(W3GP:BST1:CHAN:DPCC:TFCI STAT) to the associated values. \n
			:param sf_ormat: integer Range: 0 to dynamic
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')"""
		param = Conversions.decimal_value_to_str(sf_ormat)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:BSTation:ENHanced:CHANnel{channel_cmd_val}:DPCH:CCODing:SFORmat {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""[SOURce<HW>]:BB:W3GPp:BSTation:ENHanced:CHANnel<CH>:DPCH:CCODing:SFORmat \n
		The command sets the slot format for the selected enhanced DPCH of base station 1. The slot format is fixed for
		channel-coded measurement channels conforming to the standard - 'Reference Measurement Channel'. Changing the slot format
		automatically activates User coding (W3GP:BST:ENH:CHAN<11...13>:DPCH:CCOD:TYPE USER) . The slot format also fixes the
		symbol rate, bits per frame, pilot length and TFCI state parameters. When a channel coding type conforming to the
		standard is selected (method RsSmbv.Source.Bb.W3Gpp.Bstation.Enhanced.Channel.Dpch.Ccoding.TypePy.set) and channel coding
		is activated, the slot format is (method RsSmbv.Source.Bb.W3Gpp.Bstation.Enhanced.Channel.Dpch.Ccoding.State.
		set) automatically set to the associated value. Changing the slot format automatically activates User coding
		(W3GP:BST:ENH:CHAN<11...13>:DPCH:CCOD:TYPE USER) . The command sets the symbol rate (W3GP:BST:ENH:CHAN:DPCH:CCOD:SRAT) ,
		the bits per frame (W3GP:BST:ENH:CHAN:DPCH:CCOD:BPFR) , the pilot length (W3GP:BST1:CHAN:DPCC:PLEN) , and the TFCI state
		(W3GP:BST1:CHAN:DPCC:TFCI STAT) to the associated values. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')
			:return: sf_ormat: integer Range: 0 to dynamic"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:BSTation:ENHanced:CHANnel{channel_cmd_val}:DPCH:CCODing:SFORmat?')
		return Conversions.str_to_int(response)
