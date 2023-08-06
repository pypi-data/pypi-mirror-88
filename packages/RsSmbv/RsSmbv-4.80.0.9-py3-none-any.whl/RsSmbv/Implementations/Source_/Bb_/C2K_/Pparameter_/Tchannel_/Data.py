from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Data:
	"""Data commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("data", core, parent)

	# noinspection PyTypeChecker
	def get_rate(self) -> enums.Cdma2KdataRate:
		"""[SOURce<HW>]:BB:C2K:PPARameter:TCHannel:DATA:RATE \n
		This command sets the data rate of F-FCH and F-SCH. The set value is specific for the selected radio configuration. The
		setting takes effect only after execution of command method RsSmbv.Source.Bb.C2K.Pparameter.Execute.set. It is specific
		for the selected radio configuration. The value range depends on the frame length. If the frame length is changed so that
		the set data rate becomes invalid, the next permissible value is automatically set. The data rate affects the Walsh code
		(spreading factor) that are possible within a channel. If a data rate is changed so that the selected Walsh code becomes
		invalid, the next permissible value is automatically set. \n
			:return: rate: DR1K2| DR1K3| DR1K5| DR1K8| DR2K4| DR2K7| DR3K6| DR4K8| DR7K2| DR9K6| DR14K4| DR19K2| DR28K8| DR38K4| DR57K6| DR76K8| DR115K2| DR153K6| DR230K4| DR259K2| DR307K2| DR460K8| DR518K4| DR614K4| DR1036K8| NUSed
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:C2K:PPARameter:TCHannel:DATA:RATE?')
		return Conversions.str_to_scalar_enum(response, enums.Cdma2KdataRate)

	def set_rate(self, rate: enums.Cdma2KdataRate) -> None:
		"""[SOURce<HW>]:BB:C2K:PPARameter:TCHannel:DATA:RATE \n
		This command sets the data rate of F-FCH and F-SCH. The set value is specific for the selected radio configuration. The
		setting takes effect only after execution of command method RsSmbv.Source.Bb.C2K.Pparameter.Execute.set. It is specific
		for the selected radio configuration. The value range depends on the frame length. If the frame length is changed so that
		the set data rate becomes invalid, the next permissible value is automatically set. The data rate affects the Walsh code
		(spreading factor) that are possible within a channel. If a data rate is changed so that the selected Walsh code becomes
		invalid, the next permissible value is automatically set. \n
			:param rate: DR1K2| DR1K3| DR1K5| DR1K8| DR2K4| DR2K7| DR3K6| DR4K8| DR7K2| DR9K6| DR14K4| DR19K2| DR28K8| DR38K4| DR57K6| DR76K8| DR115K2| DR153K6| DR230K4| DR259K2| DR307K2| DR460K8| DR518K4| DR614K4| DR1036K8| NUSed
		"""
		param = Conversions.enum_scalar_to_str(rate, enums.Cdma2KdataRate)
		self._core.io.write(f'SOURce<HwInstance>:BB:C2K:PPARameter:TCHannel:DATA:RATE {param}')
