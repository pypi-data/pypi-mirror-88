from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Parameters:
	"""Parameters commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("parameters", core, parent)

	def set(self, parameters: enums.Cdma2KmpPdchFiveColDn, stream=repcap.Stream.Default, subpacket=repcap.Subpacket.Default) -> None:
		"""[SOURce<HW>]:BB:C2K:BSTation<ST>:PDCHannel:SUBPacket<DI>:PARameters \n
		Selects a fixed combination of parameters 'Bits per Encoder Packet', 'Number of 32-Chip Walsh Channels', 'Subpacket Data
		Rate', 'Number of Slots per Subpackets' and 'Modulation Order'. These combinations are shown in the following list in the
		form of a table for all five parameters. The complete range of 127 possible combinations is only available for subpacket
		1. If 'Same Packet Setup for all Subpackets' is enabled (SOUR:BB:C2K:BST2:PDCH:PSET ON) , this command is only valid for
		subpacket 1.
			Table Header: Parameter of command SOUR:BB:C2K:BST:PDCH:PAR / Number of Bits per Encoder Packet / Number of 32-Chip Walsh Channels / Subpacket Data Rate (kbps) / Number of Slots per Subpacket / Modulation Order \n
			- 1 / 2328 / 28 / 1862.4 / 1 / 8-PSK
			- 2 / 3864 / 27 / 1545.6 / 2 / QPSK
			- 3 / 3096 / 26 / 2476.8 / 1 / 16-QAM
			- 4 / 3864 / 26 / 3091.2 / 1 / 16-QAM
			- 5 / 1560 / 25 / 1248.0 / 1 / QPSK
			- 6 / 2328 / 25 / 1862.4 / 1 / 8-PSK
			- 7 / 3096 / 25 / 1238.4 / 2 / QPSK
			- 8 / 3864 / 25 / 1545.6 / 2 / 8-PSK
			- 9 / 2328 / 23 / 931.2 / 2 / QPSK
			- 10 / 2328 / 23 / 1862.4 / 1 / 16-QAM
			- 11 / 3096 / 23 / 2476.8 / 1 / 16-QAM
			- 12 / 3864 / 23 / 1545.6 / 2 / 8-PSK
			- 13 / 1560 / 22 / 1248.0 / 1 / QPSK
			- 14 / 3096 / 22 / 1238.4 / 2 / QPSK
			- 15 / 1560 / 21 / 1248.0 / 1 / 8-PSK
			- 16 / 3096 / 21 / 1238.4 / 2 / 8-PSK
			- 17 / 3096 / 21 / 2476.8 / 1 / 16-QAM
			- 18 / 3864 / 21 / 1545.6 / 2 / 8-PSK
			- 19 / 1560 / 20 / 624.0 / 2 / QPSK
			- 20 / 2328 / 20 / 465.6 / 4 / QPSK
			- 21 / 2328 / 20 / 931.2 / 2 / QPSK
			- 22 / 2328 / 20 / 1862.4 / 1 / 16-QAM
			- 23 / 3096 / 20 / 619.2 / 4 / QPSK
			- 24 / 408 / 19 / 326.4 / 1 / QPSK
			- 25 / 792 / 19 / 316.8 / 2 / QPSK
			- 26 / 792 / 19 / 633.6 / 1 / QPSK
			- 27 / 1560 / 19 / 1248.0 / 1 / 8-PSK
			- 28 / 3096 / 19 / 1238.4 / 2 / 8-PSK
			- 29 / 3864 / 19 / 772.8 / 4 / QPSK
			- 30 / 3864 / 19 / 1545.6 / 2 / 16-QAM
			- 31 / 2328 / 18 / 1862.4 / 1 / 16-QAM
			- 32 / 1560 / 17 / 1248.0 / 1 / 8-PSK
			- 33 / 2328 / 17 / 931.2 / 2 / QPSK
			- 34 / 3096 / 17 / 1238.4 / 2 / 8-PSK
			- 35 / 3864 / 17 / 1545.6 / 2 / 16-QAM
			- 36 / 2328 / 16 / 1862.4 / 1 / 16-QAM
			- 37 / 3096 / 16 / 619.2 / 4 / QPSK
			- 38 / 3864 / 16 / 772.8 / 4 / QPSK
			- 39 / 792 / 15 / 633.6 / 1 / QPSK
			- 40 / 1560 / 15 / 624.0 / 2 / QPSK
			- 41 / 1560 / 15 / 1248.0 / 1 / 16-QAM
			- 42 / 2328 / 15 / 931.2 / 2 / 8-PSK
			- 43 / 3096 / 15 / 1238.4 / 2 / 16-QAM
			- 44 / 3864 / 15 / 1545.6 / 2 / 16-QAM
			- 45 / 1560 / 14 / 312.0 / 4 / QPSK
			- 46 / 2328 / 14 / 465.6 / 4 / QPSK
			- 47 / 3864 / 14 / 772.8 / 4 / QPSK
			- 48 / 3864 / 14 / 1545.6 / 2 / 16-QAM
			- 49 / 792 / 13 / 633.6 / 1 / QPSK
			- 50 / 1560 / 13 / 624.0 / 2 / QPSK
			- 51 / 1560 / 13 / 1248.0 / 1 / 16-QAM
			- 52 / 2328 / 13 / 931.2 / 2 / 8-PSK
			- 53 / 3096 / 13 / 619.2 / 4 / QPSK
			- 54 / 3096 / 13 / 1238.4 / 2 / 16-QAM
			- 55 / 3864 / 13 / 1545.6 / 2 / 16-QAM
			- 56 / 1560 / 12 / 1248.0 / 1 / 16-QAM
			- 57 / 3096 / 12 / 1238.4 / 2 / 16-QAM
			- 58 / 3864 / 12 / 772.8 / 4 / 8-PSK
			- 59 / 408 / 11 / 326.4 / 1 / QPSK
			- 60 / 792 / 11 / 158.4 / 4 / QPSK
			- 61 / 792 / 11 / 316.8 / 2 / QPSK
			- 62 / 792 / 11 / 633.6 / 1 / QPSK
			- 63 / 1560 / 11 / 624.0 / 2 / QPSK
			- 64 / 1560 / 11 / 1248.0 / 1 / 16-QAM
			- 65 / 2328 / 11 / 465.6 / 4 / QPSK
			- 66 / 2328 / 11 / 931.2 / 2 / 16-QAM
			- 67 / 3096 / 11 / 619.2 / 4 / QPSK
			- 68 / 3096 / 11 / 1238.4 / 2 / 16-QAM
			- 69 / 3864 / 11 / 772.8 / 4 / 8-PSK
			- 70 / 792 / 10 / 633.6 / 1 / 8-PSK
			- 71 / 1560 / 10 / 624.0 / 2 / 8-PSK
			- 72 / 2328 / 10 / 931.2 / 2 / 16-QAM
			- 73 / 3096 / 10 / 619.2 / 4 / 8-PSK
			- 74 / 792 / 9 / 633.6 / 1 / 8-PSK
			- 75 / 1560 / 9 / 312.0 / 4 / QPSK
			- 76 / 1560 / 9 / 624.0 / 2 / 8-PSK
			- 77 / 2328 / 9 / 465.6 / 4 / QPSK
			- 78 / 2328 / 9 / 931.2 / 2 / 16-QAM
			- 79 / 3096 / 9 / 619.2 / 4 / 8-PSK
			- 80 / 3864 / 9 / 772.8 / 4 / 16-QAM
			- 81 / 408 / 8 / 163.2 / 2 / QPSK
			- 82 / 408 / 8 / 326.4 / 1 / QPSK
			- 83 / 792 / 8 / 316.8 / 2 / QPSK
			- 84 / 792 / 8 / 633.6 / 1 / 16-QAM
			- 85 / 1560 / 8 / 624.0 / 2 / 16-QAM
			- 86 / 2328 / 8 / 465.6 / 4 / 8-PSK
			- 87 / 2328 / 8 / 931.2 / 2 / 16-QAM
			- 88 / 3096 / 8 / 619.2 / 4 / 16-QAM
			- 89 / 3864 / 8 / 772.8 / 4 / 16-QAM
			- 90 / 408 / 7 / 326.4 / 1 / QPSK
			- 91 / 792 / 7 / 316.8 / 2 / QPSK
			- 92 / 792 / 7 / 633.6 / 1 / 16-QAM
			- 93 / 1560 / 7 / 312.0 / 4 / QPSK
			- 94 / 1560 / 7 / 624.0 / 2 / 16-QAM
			- 95 / 2328 / 7 / 465.6 / 4 / 8-PSK
			- 96 / 3096 / 7 / 619.2 / 4 / 16-QAM
			- 97 / 3864 / 7 / 772.8 / 4 / 16-QAM
			- 98 / 408 / 6 / 326.4 / 1 / QPSK
			- 99 / 792 / 6 / 158.4 / 4 / QPSK
			- 100 / 792 / 6 / 316.8 / 2 / QPSK
			- 101 / 792 / 6 / 633.6 / 1 / 16-QAM
			- 102 / 1560 / 6 / 312.0 / 4 / QPSK
			- 103 / 1560 / 6 / 624.0 / 2 / 16-QAM
			- 104 / 2328 / 6 / 465.6 / 4 / 16-QAM
			- 105 / 3096 / 6 / 619.2 / 4 / 16-QAM
			- 106 / 408 / 5 / 163.2 / 2 / QPSK
			- 107 / 408 / 5 / 326.4 / 1 / 8-PSK
			- 108 / 792 / 5 / 316.8 / 2 / 8-PSK
			- 109 / 1560 / 5 / 312.0 / 4 / 8-PSK
			- 110 / 2328 / 5 / 465.6 / 4 / 16-QAM
			- 111 / 408 / 4 / 81.6 / 4 / QPSK
			- 112 / 408 / 4 / 163.2 / 2 / QPSK
			- 113 / 408 / 4 / 326.4 / 1 / 16-QAM
			- 114 / 792 / 4 / 158.4 / 4 / QPSK
			- 115 / 792 / 4 / 316.8 / 2 / 16-QAM
			- 116 / 1560 / 4 / 312.0 / 4 / 16-QAM
			- 117 / 2328 / 4 / 465.6 / 4 / 16-QAM
			- 118 / 408 / 3 / 81.6 / 4 / QPSK
			- 119 / 408 / 3 / 163.2 / 2 / QPSK
			- 120 / 408 / 3 / 326.4 / 1 / 16-QAM
			- 121 / 792 / 3 / 158.4 / 4 / QPSK
			- 122 / 792 / 3 / 316.8 / 2 / 16-QAM
			- 123 / 1560 / 3 / 312.0 / 4 / 16-QAM
			- 124 / 408 / 2 / 81.6 / 4 / QPSK
			- 125 / 408 / 2 / 163.2 / 2 / 16-QAM
			- 126 / 792 / 2 / 158.4 / 4 / 16-QAM
			- 127 / 408 / 1 / 81.6 / 4 / 16-QAM \n
			:param parameters: 1 to 127
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param subpacket: optional repeated capability selector. Default value: Nr1 (settable in the interface 'SubPacket')"""
		param = Conversions.enum_scalar_to_str(parameters, enums.Cdma2KmpPdchFiveColDn)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		subpacket_cmd_val = self._base.get_repcap_cmd_value(subpacket, repcap.Subpacket)
		self._core.io.write(f'SOURce<HwInstance>:BB:C2K:BSTation{stream_cmd_val}:PDCHannel:SUBPacket{subpacket_cmd_val}:PARameters {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default, subpacket=repcap.Subpacket.Default) -> enums.Cdma2KmpPdchFiveColDn:
		"""[SOURce<HW>]:BB:C2K:BSTation<ST>:PDCHannel:SUBPacket<DI>:PARameters \n
		Selects a fixed combination of parameters 'Bits per Encoder Packet', 'Number of 32-Chip Walsh Channels', 'Subpacket Data
		Rate', 'Number of Slots per Subpackets' and 'Modulation Order'. These combinations are shown in the following list in the
		form of a table for all five parameters. The complete range of 127 possible combinations is only available for subpacket
		1. If 'Same Packet Setup for all Subpackets' is enabled (SOUR:BB:C2K:BST2:PDCH:PSET ON) , this command is only valid for
		subpacket 1.
			Table Header: Parameter of command SOUR:BB:C2K:BST:PDCH:PAR / Number of Bits per Encoder Packet / Number of 32-Chip Walsh Channels / Subpacket Data Rate (kbps) / Number of Slots per Subpacket / Modulation Order \n
			- 1 / 2328 / 28 / 1862.4 / 1 / 8-PSK
			- 2 / 3864 / 27 / 1545.6 / 2 / QPSK
			- 3 / 3096 / 26 / 2476.8 / 1 / 16-QAM
			- 4 / 3864 / 26 / 3091.2 / 1 / 16-QAM
			- 5 / 1560 / 25 / 1248.0 / 1 / QPSK
			- 6 / 2328 / 25 / 1862.4 / 1 / 8-PSK
			- 7 / 3096 / 25 / 1238.4 / 2 / QPSK
			- 8 / 3864 / 25 / 1545.6 / 2 / 8-PSK
			- 9 / 2328 / 23 / 931.2 / 2 / QPSK
			- 10 / 2328 / 23 / 1862.4 / 1 / 16-QAM
			- 11 / 3096 / 23 / 2476.8 / 1 / 16-QAM
			- 12 / 3864 / 23 / 1545.6 / 2 / 8-PSK
			- 13 / 1560 / 22 / 1248.0 / 1 / QPSK
			- 14 / 3096 / 22 / 1238.4 / 2 / QPSK
			- 15 / 1560 / 21 / 1248.0 / 1 / 8-PSK
			- 16 / 3096 / 21 / 1238.4 / 2 / 8-PSK
			- 17 / 3096 / 21 / 2476.8 / 1 / 16-QAM
			- 18 / 3864 / 21 / 1545.6 / 2 / 8-PSK
			- 19 / 1560 / 20 / 624.0 / 2 / QPSK
			- 20 / 2328 / 20 / 465.6 / 4 / QPSK
			- 21 / 2328 / 20 / 931.2 / 2 / QPSK
			- 22 / 2328 / 20 / 1862.4 / 1 / 16-QAM
			- 23 / 3096 / 20 / 619.2 / 4 / QPSK
			- 24 / 408 / 19 / 326.4 / 1 / QPSK
			- 25 / 792 / 19 / 316.8 / 2 / QPSK
			- 26 / 792 / 19 / 633.6 / 1 / QPSK
			- 27 / 1560 / 19 / 1248.0 / 1 / 8-PSK
			- 28 / 3096 / 19 / 1238.4 / 2 / 8-PSK
			- 29 / 3864 / 19 / 772.8 / 4 / QPSK
			- 30 / 3864 / 19 / 1545.6 / 2 / 16-QAM
			- 31 / 2328 / 18 / 1862.4 / 1 / 16-QAM
			- 32 / 1560 / 17 / 1248.0 / 1 / 8-PSK
			- 33 / 2328 / 17 / 931.2 / 2 / QPSK
			- 34 / 3096 / 17 / 1238.4 / 2 / 8-PSK
			- 35 / 3864 / 17 / 1545.6 / 2 / 16-QAM
			- 36 / 2328 / 16 / 1862.4 / 1 / 16-QAM
			- 37 / 3096 / 16 / 619.2 / 4 / QPSK
			- 38 / 3864 / 16 / 772.8 / 4 / QPSK
			- 39 / 792 / 15 / 633.6 / 1 / QPSK
			- 40 / 1560 / 15 / 624.0 / 2 / QPSK
			- 41 / 1560 / 15 / 1248.0 / 1 / 16-QAM
			- 42 / 2328 / 15 / 931.2 / 2 / 8-PSK
			- 43 / 3096 / 15 / 1238.4 / 2 / 16-QAM
			- 44 / 3864 / 15 / 1545.6 / 2 / 16-QAM
			- 45 / 1560 / 14 / 312.0 / 4 / QPSK
			- 46 / 2328 / 14 / 465.6 / 4 / QPSK
			- 47 / 3864 / 14 / 772.8 / 4 / QPSK
			- 48 / 3864 / 14 / 1545.6 / 2 / 16-QAM
			- 49 / 792 / 13 / 633.6 / 1 / QPSK
			- 50 / 1560 / 13 / 624.0 / 2 / QPSK
			- 51 / 1560 / 13 / 1248.0 / 1 / 16-QAM
			- 52 / 2328 / 13 / 931.2 / 2 / 8-PSK
			- 53 / 3096 / 13 / 619.2 / 4 / QPSK
			- 54 / 3096 / 13 / 1238.4 / 2 / 16-QAM
			- 55 / 3864 / 13 / 1545.6 / 2 / 16-QAM
			- 56 / 1560 / 12 / 1248.0 / 1 / 16-QAM
			- 57 / 3096 / 12 / 1238.4 / 2 / 16-QAM
			- 58 / 3864 / 12 / 772.8 / 4 / 8-PSK
			- 59 / 408 / 11 / 326.4 / 1 / QPSK
			- 60 / 792 / 11 / 158.4 / 4 / QPSK
			- 61 / 792 / 11 / 316.8 / 2 / QPSK
			- 62 / 792 / 11 / 633.6 / 1 / QPSK
			- 63 / 1560 / 11 / 624.0 / 2 / QPSK
			- 64 / 1560 / 11 / 1248.0 / 1 / 16-QAM
			- 65 / 2328 / 11 / 465.6 / 4 / QPSK
			- 66 / 2328 / 11 / 931.2 / 2 / 16-QAM
			- 67 / 3096 / 11 / 619.2 / 4 / QPSK
			- 68 / 3096 / 11 / 1238.4 / 2 / 16-QAM
			- 69 / 3864 / 11 / 772.8 / 4 / 8-PSK
			- 70 / 792 / 10 / 633.6 / 1 / 8-PSK
			- 71 / 1560 / 10 / 624.0 / 2 / 8-PSK
			- 72 / 2328 / 10 / 931.2 / 2 / 16-QAM
			- 73 / 3096 / 10 / 619.2 / 4 / 8-PSK
			- 74 / 792 / 9 / 633.6 / 1 / 8-PSK
			- 75 / 1560 / 9 / 312.0 / 4 / QPSK
			- 76 / 1560 / 9 / 624.0 / 2 / 8-PSK
			- 77 / 2328 / 9 / 465.6 / 4 / QPSK
			- 78 / 2328 / 9 / 931.2 / 2 / 16-QAM
			- 79 / 3096 / 9 / 619.2 / 4 / 8-PSK
			- 80 / 3864 / 9 / 772.8 / 4 / 16-QAM
			- 81 / 408 / 8 / 163.2 / 2 / QPSK
			- 82 / 408 / 8 / 326.4 / 1 / QPSK
			- 83 / 792 / 8 / 316.8 / 2 / QPSK
			- 84 / 792 / 8 / 633.6 / 1 / 16-QAM
			- 85 / 1560 / 8 / 624.0 / 2 / 16-QAM
			- 86 / 2328 / 8 / 465.6 / 4 / 8-PSK
			- 87 / 2328 / 8 / 931.2 / 2 / 16-QAM
			- 88 / 3096 / 8 / 619.2 / 4 / 16-QAM
			- 89 / 3864 / 8 / 772.8 / 4 / 16-QAM
			- 90 / 408 / 7 / 326.4 / 1 / QPSK
			- 91 / 792 / 7 / 316.8 / 2 / QPSK
			- 92 / 792 / 7 / 633.6 / 1 / 16-QAM
			- 93 / 1560 / 7 / 312.0 / 4 / QPSK
			- 94 / 1560 / 7 / 624.0 / 2 / 16-QAM
			- 95 / 2328 / 7 / 465.6 / 4 / 8-PSK
			- 96 / 3096 / 7 / 619.2 / 4 / 16-QAM
			- 97 / 3864 / 7 / 772.8 / 4 / 16-QAM
			- 98 / 408 / 6 / 326.4 / 1 / QPSK
			- 99 / 792 / 6 / 158.4 / 4 / QPSK
			- 100 / 792 / 6 / 316.8 / 2 / QPSK
			- 101 / 792 / 6 / 633.6 / 1 / 16-QAM
			- 102 / 1560 / 6 / 312.0 / 4 / QPSK
			- 103 / 1560 / 6 / 624.0 / 2 / 16-QAM
			- 104 / 2328 / 6 / 465.6 / 4 / 16-QAM
			- 105 / 3096 / 6 / 619.2 / 4 / 16-QAM
			- 106 / 408 / 5 / 163.2 / 2 / QPSK
			- 107 / 408 / 5 / 326.4 / 1 / 8-PSK
			- 108 / 792 / 5 / 316.8 / 2 / 8-PSK
			- 109 / 1560 / 5 / 312.0 / 4 / 8-PSK
			- 110 / 2328 / 5 / 465.6 / 4 / 16-QAM
			- 111 / 408 / 4 / 81.6 / 4 / QPSK
			- 112 / 408 / 4 / 163.2 / 2 / QPSK
			- 113 / 408 / 4 / 326.4 / 1 / 16-QAM
			- 114 / 792 / 4 / 158.4 / 4 / QPSK
			- 115 / 792 / 4 / 316.8 / 2 / 16-QAM
			- 116 / 1560 / 4 / 312.0 / 4 / 16-QAM
			- 117 / 2328 / 4 / 465.6 / 4 / 16-QAM
			- 118 / 408 / 3 / 81.6 / 4 / QPSK
			- 119 / 408 / 3 / 163.2 / 2 / QPSK
			- 120 / 408 / 3 / 326.4 / 1 / 16-QAM
			- 121 / 792 / 3 / 158.4 / 4 / QPSK
			- 122 / 792 / 3 / 316.8 / 2 / 16-QAM
			- 123 / 1560 / 3 / 312.0 / 4 / 16-QAM
			- 124 / 408 / 2 / 81.6 / 4 / QPSK
			- 125 / 408 / 2 / 163.2 / 2 / 16-QAM
			- 126 / 792 / 2 / 158.4 / 4 / 16-QAM
			- 127 / 408 / 1 / 81.6 / 4 / 16-QAM \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param subpacket: optional repeated capability selector. Default value: Nr1 (settable in the interface 'SubPacket')
			:return: parameters: 1 to 127"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		subpacket_cmd_val = self._base.get_repcap_cmd_value(subpacket, repcap.Subpacket)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:C2K:BSTation{stream_cmd_val}:PDCHannel:SUBPacket{subpacket_cmd_val}:PARameters?')
		return Conversions.str_to_scalar_enum(response, enums.Cdma2KmpPdchFiveColDn)
