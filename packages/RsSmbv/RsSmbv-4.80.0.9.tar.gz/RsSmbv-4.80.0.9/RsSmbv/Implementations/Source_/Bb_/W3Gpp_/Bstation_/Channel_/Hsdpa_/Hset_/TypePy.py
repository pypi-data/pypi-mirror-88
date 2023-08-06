from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TypePy:
	"""TypePy commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("typePy", core, parent)

	def set(self, type_py: enums.HsHsetScchType, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:BSTation<ST>:CHANnel<CH>:HSDPa:HSET:TYPE \n
		Sets the HS-SCCH type. \n
			:param type_py: NORMal| LOPeration| MIMO NORMal Normal operation mode. LOPeration HS-SCCH less operation mode. MIMO HS-SCCH Type 3 mode is defined for MIMO operation. Enabling this operation mode, enables the MIMO parameters method RsSmbv.Source.Bb.W3Gpp.Bstation.Channel.Hsdpa.Mimo.Cvpb.set, method RsSmbv.Source.Bb.W3Gpp.Bstation.Channel.Hsdpa.Mimo.Modulation.set, method RsSmbv.Source.Bb.W3Gpp.Bstation.Channel.Hsdpa.Mimo.PwPattern.set and method RsSmbv.Source.Bb.W3Gpp.Bstation.Channel.Hsdpa.Mimo.StaPattern.set and all Stream 2 parameters.
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')"""
		param = Conversions.enum_scalar_to_str(type_py, enums.HsHsetScchType)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:CHANnel{channel_cmd_val}:HSDPa:HSET:TYPE {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> enums.HsHsetScchType:
		"""[SOURce<HW>]:BB:W3GPp:BSTation<ST>:CHANnel<CH>:HSDPa:HSET:TYPE \n
		Sets the HS-SCCH type. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')
			:return: type_py: NORMal| LOPeration| MIMO NORMal Normal operation mode. LOPeration HS-SCCH less operation mode. MIMO HS-SCCH Type 3 mode is defined for MIMO operation. Enabling this operation mode, enables the MIMO parameters method RsSmbv.Source.Bb.W3Gpp.Bstation.Channel.Hsdpa.Mimo.Cvpb.set, method RsSmbv.Source.Bb.W3Gpp.Bstation.Channel.Hsdpa.Mimo.Modulation.set, method RsSmbv.Source.Bb.W3Gpp.Bstation.Channel.Hsdpa.Mimo.PwPattern.set and method RsSmbv.Source.Bb.W3Gpp.Bstation.Channel.Hsdpa.Mimo.StaPattern.set and all Stream 2 parameters."""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:CHANnel{channel_cmd_val}:HSDPa:HSET:TYPE?')
		return Conversions.str_to_scalar_enum(response, enums.HsHsetScchType)
