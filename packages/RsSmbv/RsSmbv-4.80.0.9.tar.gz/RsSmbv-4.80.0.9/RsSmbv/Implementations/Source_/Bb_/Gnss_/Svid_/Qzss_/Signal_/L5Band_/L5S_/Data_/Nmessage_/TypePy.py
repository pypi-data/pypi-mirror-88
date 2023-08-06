from ............Internal.Core import Core
from ............Internal.CommandsGroup import CommandsGroup
from ............Internal import Conversions
from ............ import enums
from ............ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TypePy:
	"""TypePy commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("typePy", core, parent)

	def set(self, data: enums.DataSourGnss, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:SVID<CH>:QZSS<ST>:SIGNal:L5Band:L5S:DATA:NMESsage:TYPE \n
		Sets the data source used for the generation of the navigation message. \n
			:param data: ZERO| ONE| PATTern| PN9| PN11| PN15| PN16| PN20| PN21| PN23| DLISt| RNData| ZNData ZERO|ONE|PATTern|PN9|PN11|PN15|PN16|PN20|PN21|PN23|DLISt Arbitrary data source. Define the pattern and load an existing data list file with the commands: method RsSmbv.Source.Bb.Gnss.Svid.Gps.Signal.L1Band.Ca.Data.Nmessage.Pattern.set method RsSmbv.Source.Bb.Gnss.Svid.Gps.Signal.L1Band.Ca.Data.Nmessage.Dselect.set RNData Summary indication for real navigation data. Current navigation message type depends on the GNSS system and the RF band, e.g. for GPS in L1 RNData means LNAV. ZNData Zero navigation data Sets the orbit and clock correction parameters in the broadcasted navigation message to zero.
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Qzss')"""
		param = Conversions.enum_scalar_to_str(data, enums.DataSourGnss)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:QZSS{stream_cmd_val}:SIGNal:L5Band:L5S:DATA:NMESsage:TYPE {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> enums.DataSourGnss:
		"""[SOURce<HW>]:BB:GNSS:SVID<CH>:QZSS<ST>:SIGNal:L5Band:L5S:DATA:NMESsage:TYPE \n
		Sets the data source used for the generation of the navigation message. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Qzss')
			:return: data: ZERO| ONE| PATTern| PN9| PN11| PN15| PN16| PN20| PN21| PN23| DLISt| RNData| ZNData ZERO|ONE|PATTern|PN9|PN11|PN15|PN16|PN20|PN21|PN23|DLISt Arbitrary data source. Define the pattern and load an existing data list file with the commands: method RsSmbv.Source.Bb.Gnss.Svid.Gps.Signal.L1Band.Ca.Data.Nmessage.Pattern.set method RsSmbv.Source.Bb.Gnss.Svid.Gps.Signal.L1Band.Ca.Data.Nmessage.Dselect.set RNData Summary indication for real navigation data. Current navigation message type depends on the GNSS system and the RF band, e.g. for GPS in L1 RNData means LNAV. ZNData Zero navigation data Sets the orbit and clock correction parameters in the broadcasted navigation message to zero."""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:QZSS{stream_cmd_val}:SIGNal:L5Band:L5S:DATA:NMESsage:TYPE?')
		return Conversions.str_to_scalar_enum(response, enums.DataSourGnss)
