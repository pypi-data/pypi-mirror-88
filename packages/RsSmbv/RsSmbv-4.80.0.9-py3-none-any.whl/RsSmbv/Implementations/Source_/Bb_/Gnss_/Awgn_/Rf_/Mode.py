from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mode:
	"""Mode commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mode", core, parent)

	def set(self, awgn_mode: enums.NoisAwgnMode, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:AWGN:[RF<CH>]:MODE \n
		Activates/deactivates the generation of an AWGN signal. The interferer (AWGN or CW interferer, depending on the selected
		mode) is generated after the generator is activated. \n
			:param awgn_mode: ADD| CW
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rf')"""
		param = Conversions.enum_scalar_to_str(awgn_mode, enums.NoisAwgnMode)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:AWGN:RF{channel_cmd_val}:MODE {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.NoisAwgnMode:
		"""[SOURce<HW>]:BB:GNSS:AWGN:[RF<CH>]:MODE \n
		Activates/deactivates the generation of an AWGN signal. The interferer (AWGN or CW interferer, depending on the selected
		mode) is generated after the generator is activated. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rf')
			:return: awgn_mode: ADD| CW"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:AWGN:RF{channel_cmd_val}:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.NoisAwgnMode)
