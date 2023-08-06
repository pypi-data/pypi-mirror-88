import logging

from typing import Optional, Dict, List

from asyncio import TimeoutError
from asyncio.events import AbstractEventLoop

from Foundation import (
        CBUUID,
        CBService,
        CBMutableService,
        CBMutableCharacteristic
        )

from bleak.backends.service import BleakGATTService
from bleak.backends.corebluetooth.service import (
        BleakGATTServiceCoreBluetooth
        )

from .PeripheralManagerDelegate import (
        PeripheralManagerDelegate
        )
from bless.exceptions import BlessError
from bless.backends.server import BaseBlessServer
from bless.backends.corebluetooth.characteristic import (
        BlessGATTCharacteristicCoreBluetooth
        )
from bless.backends.characteristic import GattCharacteristicsFlags


logger = logging.getLogger(name=__name__)


class BlessServerCoreBluetooth(BaseBlessServer):
    """
    CoreBluetooth Implementation of BlessServer

    This implementation essentially wraps the PeripheralManagerDelegate Class
    from CoreBluetooth

    Attributes
    ----------
    name : str
        The name of the server to advertise
    services : BleakGATTServiceCollection
        A collection of services to be advertised by this server
    peripheral_manager_delegate : PeripheralManagerDelegate
        The delegated class to manage this peripheral device
    """

    def __init__(self, name: str, loop: AbstractEventLoop = None, **kwargs):
        super(BlessServerCoreBluetooth, self).__init__(loop=loop, **kwargs)

        self.name: str = name
        self.services: Dict[str, BleakGATTServiceCoreBluetooth] = {}

        self.peripheral_manager_delegate: PeripheralManagerDelegate = (
                PeripheralManagerDelegate.alloc().init()
                )
        self.peripheral_manager_delegate.read_request_func = self.read_request
        self.peripheral_manager_delegate.write_request_func = (
                self.write_request
                )

    async def start(self, timeout: float = 10):
        """
        Start the server

        Parameters
        ----------
        timeout : float
            Floating point decimal in seconds for how long to wait for the
            on-board bluetooth module to power on
        """
        await self.peripheral_manager_delegate.wait_for_powered_on(timeout)

        for service_uuid in self.services:
            bleak_service: BleakGATTService = self.services[service_uuid]
            service_obj: CBService = bleak_service.obj
            logger.debug("Adding service: {}".format(bleak_service.uuid))
            await self.peripheral_manager_delegate.addService(service_obj)

        if not self.read_request_func or not self.write_request_func:
            raise BlessError("Callback functions must be initialized first")

        advertisement_data = {
            "kCBAdvDataServiceUUIDs": list(
                map(lambda x: self.services[x].obj.UUID(), self.services)
                ),
            "kCBAdvDataLocalName": self.name
            }
        logger.debug("Advertisement Data: {}".format(advertisement_data))
        try:
            await self.peripheral_manager_delegate.startAdvertising_(
                    advertisement_data
                    )
        except TimeoutError:
            # If advertising fails as a result of bluetooth module power
            # cycling or advertisement failure, attempt to start again
            await self.start()

        logger.debug("Advertising...")

    async def stop(self):
        """
        Stop the server
        """
        await self.peripheral_manager_delegate.stopAdvertising()

    async def is_connected(self) -> bool:
        """
        Determine whether there are any connected central devices

        Returns
        -------
        bool
            True if there are central devices that are connected
        """
        n_subscriptions = len(
                self.peripheral_manager_delegate._central_subscriptions
                )
        return n_subscriptions > 0

    async def is_advertising(self) -> bool:
        """
        Determine whether the service is advertising

        Returns
        -------
        bool
            True if advertising
        """
        return self.peripheral_manager_delegate.is_advertising() == 1

    async def add_new_service(self, uuid: str):
        """
        Add a service and all it's characteristics to be advertised

        Parameters
        ----------
        uuid : str
            The string representation of the UUID of the service to be added
        """
        logger.debug("Creating a new service with uuid: {}".format(uuid))

        service_uuid: CBUUID = CBUUID.alloc().initWithString_(uuid)
        cb_service: CBMutableService = (
                CBMutableService.alloc().initWithType_primary_(
                    service_uuid,
                    True
                    )
                )

        bleak_service: BleakGATTServiceCoreBluetooth = (
                BleakGATTServiceCoreBluetooth(obj=cb_service)
                )

        self.services[uuid] = bleak_service

    async def add_new_characteristic(
            self,
            service_uuid: str,
            char_uuid: str,
            properties: GattCharacteristicsFlags,
            value: Optional[bytearray],
            permissions: int
            ):
        """
        Generate a new characteristic to be associated with the server

        Parameters
        ----------
        service_uuid: str
            The string representation of the UUID for the service associated
            with the characteristic to be added
        char_uuid : str
            The string representation of the UUID for the characteristic to be
            added
        properties : GattCharacteristicsFlags
            The flags for the characteristic
        value : Optional[bytearray]
            The initial value for the characteristic
        permissions : int
            The permissions for the characteristic
        """
        logger.debug(
                "Craeting a new characteristic with uuid: {}".format(char_uuid)
                )
        cb_uuid: CBUUID = CBUUID.alloc().initWithString_(char_uuid)
        cb_characteristic: CBMutableCharacteristic = (
                CBMutableCharacteristic.alloc()
                .initWithType_properties_value_permissions_(
                    cb_uuid,
                    properties,
                    value,
                    permissions
                    )
                )
        bleak_characteristic: BlessGATTCharacteristicCoreBluetooth = (
                BlessGATTCharacteristicCoreBluetooth(obj=cb_characteristic)
                )

        service: BleakGATTService = self.services[service_uuid]
        service.add_characteristic(bleak_characteristic)
        characteristics: List[CBMutableCharacteristic] = [
                characteristic.obj
                for characteristic in service.characteristics
                ]
        service.obj.setCharacteristics_(characteristics)

    def update_value(self, service_uuid: str, char_uuid: str) -> bool:
        """
        Update the characteristic value. This is different than using
        characteristic.set_value. This send notifications to subscribed
        central devices.

        Parameters
        ----------
        service_uuid : str
            The string representation of the UUID for the service associated
            with the characteristic to be added
        char_uuid : str
            The string representation of the UUID for the characteristic to be
            added

        Returns
        -------
        bool
            Whether the value was successfully updated
        """
        characteristic: BlessGATTCharacteristicCoreBluetooth = (
                self.services[service_uuid].get_characteristic(
                    char_uuid.lower()
                    )
                )

        value: bytes = characteristic.value
        value = value if value is not None else b'\x00'
        result: bool = (
                self.peripheral_manager_delegate
                    .peripheral_manager
                    .updateValue_forCharacteristic_onSubscribedCentrals_(
                        value,
                        characteristic.obj,
                        None
                        )
                    )

        return result
