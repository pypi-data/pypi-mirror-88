from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Types import DataType
from ......Internal.ArgSingleList import ArgSingleList
from ......Internal.ArgSingle import ArgSingle
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Value:
	"""Value commands group definition. 3 total commands, 2 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("value", core, parent)

	def clone(self) -> 'Value':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Value(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def level(self):
		"""level commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_level'):
			from .Value_.Level import Level
			self._level = Level(self._core, self._base)
		return self._level

	@property
	def pep(self):
		"""pep commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pep'):
			from .Value_.Pep import Pep
			self._pep = Pep(self._core, self._base)
		return self._pep

	def get(self, xvalue: float, xunit: enums.Unknown, stream=repcap.Stream.Default) -> float:
		"""[SOURce<HW>]:IQ:DPD<ST>:AMPM:VALue \n
		Queries the delta phase and delta power values for the selected <xValue>. \n
			:param xvalue: float Value on the x-axis Value range depends on the selected PEPinMin and PEPinMax values. Range: -100 to 100
			:param xunit: DBM| V
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Dpd')
			:return: delta_phase: float Range: -180 to 180"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('xvalue', xvalue, DataType.Float), ArgSingle('xunit', xunit, DataType.Enum))
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:IQ:DPD{stream_cmd_val}:AMPM:VALue? {param}'.rstrip())
		return Conversions.str_to_float(response)
