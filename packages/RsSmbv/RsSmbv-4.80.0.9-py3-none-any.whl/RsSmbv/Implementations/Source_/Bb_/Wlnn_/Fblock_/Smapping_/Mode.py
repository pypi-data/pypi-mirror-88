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

	def set(self, mode: enums.WlannFbSpatMapMode, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:SMAPping:MODE \n
		Selects the spatial mapping mode for the selected frame block. Except of the beamforming mode, the matrix element values
		are loaded by using info class methods. \n
			:param mode: OFF| DIRect| EXPansion| BEAMforming| INDirect OFF (only 'LEGACY' mode) The spatial mapping mode is switched off automatically. DIRect (only active with physical modes MIXED MODE or GREEN FIELD when NTX = NSTS) The transmit matrix is a CSD matrix, that is, diagonal matrix of unit magnitude and complex values that represent cyclic shifts in the time domain. EXPansion (only active with physical modes MIXED MODE or GREEN FIELD) The transmit matrix is the product of a CSD matrix and a square matrix formed of orthogonal columns, as defined in the IEEE 802.11n specification. INDirect (only active with physical modes MIXED MODE or GREEN FIELD) The transmit matrix is the product of a CSD matrix and the Hadamard unitary matrix.
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')"""
		param = Conversions.enum_scalar_to_str(mode, enums.WlannFbSpatMapMode)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:SMAPping:MODE {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.WlannFbSpatMapMode:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:SMAPping:MODE \n
		Selects the spatial mapping mode for the selected frame block. Except of the beamforming mode, the matrix element values
		are loaded by using info class methods. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: mode: OFF| DIRect| EXPansion| BEAMforming| INDirect OFF (only 'LEGACY' mode) The spatial mapping mode is switched off automatically. DIRect (only active with physical modes MIXED MODE or GREEN FIELD when NTX = NSTS) The transmit matrix is a CSD matrix, that is, diagonal matrix of unit magnitude and complex values that represent cyclic shifts in the time domain. EXPansion (only active with physical modes MIXED MODE or GREEN FIELD) The transmit matrix is the product of a CSD matrix and a square matrix formed of orthogonal columns, as defined in the IEEE 802.11n specification. INDirect (only active with physical modes MIXED MODE or GREEN FIELD) The transmit matrix is the product of a CSD matrix and the Hadamard unitary matrix."""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:SMAPping:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.WlannFbSpatMapMode)
