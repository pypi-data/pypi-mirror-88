from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tdiversity:
	"""Tdiversity commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tdiversity", core, parent)

	def clone(self) -> 'Tdiversity':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Tdiversity(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def mode(self):
		"""mode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mode'):
			from .Tdiversity_.Mode import Mode
			self._mode = Mode(self._core, self._base)
		return self._mode

	def set(self, tdiversity: enums.Cdma2KtxDiv, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:C2K:BSTation<ST>:TDIVersity \n
		The command activates and deactivates signal calculation with transmit diversity (OFF) . To activate transmit diversity,
		the antenna must be specified whose signals are to be simulated (ANT1 or ANT2) . The diversity scheme is selected using
		command method RsSmbv.Source.Bb.C2K.Bstation.Tdiversity.Mode.set. \n
			:param tdiversity: OFF| ANT1| ANT2 OFF No transmit diversity. ANT1 Calculate and apply the output signal for antenna 1. ANT2 Calculate and apply the output signal for antenna 2.
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')"""
		param = Conversions.enum_scalar_to_str(tdiversity, enums.Cdma2KtxDiv)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:C2K:BSTation{stream_cmd_val}:TDIVersity {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.Cdma2KtxDiv:
		"""[SOURce<HW>]:BB:C2K:BSTation<ST>:TDIVersity \n
		The command activates and deactivates signal calculation with transmit diversity (OFF) . To activate transmit diversity,
		the antenna must be specified whose signals are to be simulated (ANT1 or ANT2) . The diversity scheme is selected using
		command method RsSmbv.Source.Bb.C2K.Bstation.Tdiversity.Mode.set. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:return: tdiversity: OFF| ANT1| ANT2 OFF No transmit diversity. ANT1 Calculate and apply the output signal for antenna 1. ANT2 Calculate and apply the output signal for antenna 2."""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:C2K:BSTation{stream_cmd_val}:TDIVersity?')
		return Conversions.str_to_scalar_enum(response, enums.Cdma2KtxDiv)
