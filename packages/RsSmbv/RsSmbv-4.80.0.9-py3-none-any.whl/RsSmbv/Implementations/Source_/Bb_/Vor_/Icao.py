from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Icao:
	"""Icao commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("icao", core, parent)

	# noinspection PyTypeChecker
	def get_channel(self) -> enums.AvionicVorIcaoChan:
		"""[SOURce<HW>]:[BB]:VOR:ICAO:CHANnel \n
		Sets the ICAO channel and the corresponding transmitting frequency. If avionic standard modulation is activated and you
		change the 'RF Frequency', the frequency value of the closest ICAO channel is applied automatically. The 'ICAO Channel'
		is also updated. The carrier frequency is set automatically to the value of the ICAO channel. For an overview of the VOR
		ICAO channel frequencies, see 'VOR Channel Frequencies '. \n
			:return: channel: CH17X| CH17Y| CH19X| CH19Y| CH21X| CH21Y| CH23X| CH23Y| CH25X| CH25Y| CH27X| CH27Y| CH29X| CH29Y| CH31X| CH31Y| CH33X| CH33Y| CH35X| CH35Y| CH37X| CH37Y| CH39X| CH39Y| CH41X| CH41Y| CH43X| CH43Y| CH45X| CH45Y| CH47X| CH47Y| CH49X| CH49Y| CH51X| CH51Y| CH53X| CH53Y| CH55X| CH55Y| CH57X| CH57Y| CH58X| CH58Y| CH59X| CH59Y| CH70X| CH70Y| CH71X| CH71Y| CH72X| CH72Y| CH73X| CH73Y| CH74X| CH74Y| CH75X| CH75Y| CH76X| CH76Y| CH77X| CH77Y| CH78X| CH78Y| CH79X| CH79Y| CH80X| CH80Y| CH81X| CH81Y| CH82X| CH82Y| CH83X| CH83Y| CH84X| CH84Y| CH85X| CH85Y| CH86X| CH86Y| CH87X| CH87Y| CH88X| CH88Y| CH89X| CH89Y| CH90X| CH90Y| CH91X| CH91Y| CH92X| CH92Y| CH93X| CH93Y| CH94X| CH94Y| CH95X| CH95Y| CH96X| CH96Y| CH97X| CH97Y| CH98X| CH98Y| CH99X| CH99Y| CH100X| CH100Y| CH101X| CH101Y| CH102X| CH102Y| CH103X| CH103Y| CH104X| CH104Y| CH105X| CH105Y| CH106X| CH106Y| CH107X| CH107Y| CH108X| CH108Y| CH109X| CH109Y| CH110X| CH110Y| CH111X| CH111Y| CH112X| CH112Y| CH113X| CH113Y| CH114X| CH114Y| CH115X| CH115Y| CH116X| CH116Y| CH117X| CH117Y| CH118X| CH118Y| CH119X| CH119Y| CH120X| CH120Y| CH121X| CH121Y| CH122X| CH122Y| CH123X| CH123Y| CH124X| CH124Y| CH125X| CH125Y| CH126X| CH126Y
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:VOR:ICAO:CHANnel?')
		return Conversions.str_to_scalar_enum(response, enums.AvionicVorIcaoChan)

	def set_channel(self, channel: enums.AvionicVorIcaoChan) -> None:
		"""[SOURce<HW>]:[BB]:VOR:ICAO:CHANnel \n
		Sets the ICAO channel and the corresponding transmitting frequency. If avionic standard modulation is activated and you
		change the 'RF Frequency', the frequency value of the closest ICAO channel is applied automatically. The 'ICAO Channel'
		is also updated. The carrier frequency is set automatically to the value of the ICAO channel. For an overview of the VOR
		ICAO channel frequencies, see 'VOR Channel Frequencies '. \n
			:param channel: CH17X| CH17Y| CH19X| CH19Y| CH21X| CH21Y| CH23X| CH23Y| CH25X| CH25Y| CH27X| CH27Y| CH29X| CH29Y| CH31X| CH31Y| CH33X| CH33Y| CH35X| CH35Y| CH37X| CH37Y| CH39X| CH39Y| CH41X| CH41Y| CH43X| CH43Y| CH45X| CH45Y| CH47X| CH47Y| CH49X| CH49Y| CH51X| CH51Y| CH53X| CH53Y| CH55X| CH55Y| CH57X| CH57Y| CH58X| CH58Y| CH59X| CH59Y| CH70X| CH70Y| CH71X| CH71Y| CH72X| CH72Y| CH73X| CH73Y| CH74X| CH74Y| CH75X| CH75Y| CH76X| CH76Y| CH77X| CH77Y| CH78X| CH78Y| CH79X| CH79Y| CH80X| CH80Y| CH81X| CH81Y| CH82X| CH82Y| CH83X| CH83Y| CH84X| CH84Y| CH85X| CH85Y| CH86X| CH86Y| CH87X| CH87Y| CH88X| CH88Y| CH89X| CH89Y| CH90X| CH90Y| CH91X| CH91Y| CH92X| CH92Y| CH93X| CH93Y| CH94X| CH94Y| CH95X| CH95Y| CH96X| CH96Y| CH97X| CH97Y| CH98X| CH98Y| CH99X| CH99Y| CH100X| CH100Y| CH101X| CH101Y| CH102X| CH102Y| CH103X| CH103Y| CH104X| CH104Y| CH105X| CH105Y| CH106X| CH106Y| CH107X| CH107Y| CH108X| CH108Y| CH109X| CH109Y| CH110X| CH110Y| CH111X| CH111Y| CH112X| CH112Y| CH113X| CH113Y| CH114X| CH114Y| CH115X| CH115Y| CH116X| CH116Y| CH117X| CH117Y| CH118X| CH118Y| CH119X| CH119Y| CH120X| CH120Y| CH121X| CH121Y| CH122X| CH122Y| CH123X| CH123Y| CH124X| CH124Y| CH125X| CH125Y| CH126X| CH126Y
		"""
		param = Conversions.enum_scalar_to_str(channel, enums.AvionicVorIcaoChan)
		self._core.io.write(f'SOURce<HwInstance>:BB:VOR:ICAO:CHANnel {param}')
