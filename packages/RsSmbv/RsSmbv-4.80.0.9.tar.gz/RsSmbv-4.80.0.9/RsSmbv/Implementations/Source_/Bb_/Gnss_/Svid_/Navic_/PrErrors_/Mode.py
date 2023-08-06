from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mode:
	"""Mode commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mode", core, parent)

	def set(self, pr_erors_mode: enums.PseudorangeMode, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:SVID<CH>:NAVic<ST>:PRERrors:MODE \n
		Sets how the pseudorange errors are defined. \n
			:param pr_erors_mode: FSBas| CONStant| PROFile FSBas Extracted form the imported SBAS corrections, if method RsSmbv.Source.Bb.Gnss.ecModeSYNC. CONStant Set with the command method RsSmbv.Source.Bb.Gnss.Svid.Gps.PrErrors.Value.set PROFile Defined with the command pairs method RsSmbv.Source.Bb.Gnss.Svid.Gps.PrErrors.Profile.Reference.set and method RsSmbv.Source.Bb.Gnss.Svid.Gps.PrErrors.Profile.Value.set
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Navic')"""
		param = Conversions.enum_scalar_to_str(pr_erors_mode, enums.PseudorangeMode)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:NAVic{stream_cmd_val}:PRERrors:MODE {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> enums.PseudorangeMode:
		"""[SOURce<HW>]:BB:GNSS:SVID<CH>:NAVic<ST>:PRERrors:MODE \n
		Sets how the pseudorange errors are defined. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Svid')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Navic')
			:return: pr_erors_mode: FSBas| CONStant| PROFile FSBas Extracted form the imported SBAS corrections, if method RsSmbv.Source.Bb.Gnss.ecModeSYNC. CONStant Set with the command method RsSmbv.Source.Bb.Gnss.Svid.Gps.PrErrors.Value.set PROFile Defined with the command pairs method RsSmbv.Source.Bb.Gnss.Svid.Gps.PrErrors.Profile.Reference.set and method RsSmbv.Source.Bb.Gnss.Svid.Gps.PrErrors.Profile.Value.set"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:SVID{channel_cmd_val}:NAVic{stream_cmd_val}:PRERrors:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.PseudorangeMode)
