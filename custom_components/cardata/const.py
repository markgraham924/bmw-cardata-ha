"""Constants for the BMW CarData integration."""

DOMAIN = "cardata"
DEFAULT_SCOPE = "authenticate_user openid cardata:api:read cardata:streaming:read"
DEVICE_CODE_URL = "https://customer.bmwgroup.com/gcdm/oauth/device/code"
TOKEN_URL = "https://customer.bmwgroup.com/gcdm/oauth/token"
API_BASE_URL = "https://api-cardata.bmwgroup.com"
API_VERSION = "v1"
BASIC_DATA_ENDPOINT = "/customers/vehicles/{vin}/basicData"
DEFAULT_STREAM_HOST = "customer.streaming-cardata.bmwgroup.com"
DEFAULT_STREAM_PORT = 9000
DEFAULT_REFRESH_INTERVAL = 45 * 60  #How often to refresh the auth tokens in seconds
MQTT_KEEPALIVE = 30
DEBUG_LOG = True
DIAGNOSTIC_LOG_INTERVAL = 30 # How often we print stream logs in seconds
BOOTSTRAP_COMPLETE = "bootstrap_complete"
REQUEST_LOG = "request_log"
REQUEST_LOG_VERSION = 1
REQUEST_LIMIT = 50 # API Quota
REQUEST_WINDOW_SECONDS = 24 * 60 * 60 # How long API Quota is reserved after API Call in seconds
TELEMATIC_POLL_INTERVAL = 40 * 60 # How often to call the Telematic API in seconds
VEHICLE_METADATA = "vehicle_metadata"
OPTION_MQTT_KEEPALIVE = "mqtt_keepalive"
OPTION_DEBUG_LOG = "debug_log"
OPTION_DIAGNOSTIC_INTERVAL = "diagnostic_log_interval"

HV_BATTERY_CONTAINER_NAME = "BimmerData Vehicle Telemetry"
HV_BATTERY_CONTAINER_PURPOSE = "Vehicle telemetry for Home Assistant"
HV_BATTERY_DESCRIPTORS = [
    # Vehicle identity and device metadata
    "vehicle.vehicleIdentification.basicVehicleData",
    "vehicle.vehicle.travelledDistance",
    "vehicle.vehicle.avgSpeed",
    "vehicle.vehicle.deepSleepModeActive",
    "vehicle.vehicle.timeSetting",
    "vehicle.isMoving",
    "vehicle.drivetrain.engine.isActive",
    "vehicle.drivetrain.engine.isIgnitionOn",
    "vehicle.channel.ngtp.timeVehicle",
    "vehicle.cabin.infotainment.isMobilePhoneConnected",
    "vehicle.cabin.infotainment.displayUnit.distance",
    "vehicle.cabin.infotainment.hmi.distanceUnit",
    # Device tracker / GPS
    "vehicle.cabin.infotainment.navigation.currentLocation.latitude",
    "vehicle.cabin.infotainment.navigation.currentLocation.longitude",
    "vehicle.cabin.infotainment.navigation.currentLocation.heading",
    "vehicle.cabin.infotainment.navigation.currentLocation.altitude",
    "vehicle.cabin.infotainment.navigation.currentLocation.fixStatus",
    "vehicle.cabin.infotainment.navigation.currentLocation.numberOfSatellites",
    "vehicle.cabin.infotainment.navigation.destinationSet.latitude",
    "vehicle.cabin.infotainment.navigation.destinationSet.longitude",
    "vehicle.cabin.infotainment.navigation.destinationSet.arrivalTime",
    "vehicle.cabin.infotainment.navigation.remainingRange",
    "vehicle.cabin.infotainment.navigation.pointsOfInterests.max",
    # Closures, locks and access points
    "vehicle.cabin.door.lock.status",
    "vehicle.cabin.door.status",
    "vehicle.cabin.door.row1.driver.isOpen",
    "vehicle.cabin.door.row1.driver.position",
    "vehicle.cabin.door.row1.passenger.isOpen",
    "vehicle.cabin.door.row1.passenger.position",
    "vehicle.cabin.door.row2.driver.isOpen",
    "vehicle.cabin.door.row2.driver.position",
    "vehicle.cabin.door.row2.passenger.isOpen",
    "vehicle.cabin.door.row2.passenger.position",
    "vehicle.cabin.window.row1.driver.status",
    "vehicle.cabin.window.row1.passenger.status",
    "vehicle.cabin.window.row2.driver.status",
    "vehicle.cabin.window.row2.passenger.status",
    "vehicle.body.hood.isOpen",
    "vehicle.body.trunk.door.isOpen",
    "vehicle.body.trunk.isOpen",
    "vehicle.body.trunk.isLocked",
    "vehicle.body.trunk.left.door.isOpen",
    "vehicle.body.trunk.lower.door.isOpen",
    "vehicle.body.trunk.right.door.isOpen",
    "vehicle.body.trunk.upper.door.isOpen",
    "vehicle.body.trunk.window.isOpen",
    "vehicle.cabin.sunroof.status",
    "vehicle.cabin.sunroof.overallStatus",
    "vehicle.cabin.sunroof.tiltStatus",
    # Lighting and alarms
    "vehicle.body.lights.isRunningOn",
    "vehicle.vehicle.antiTheftAlarmSystem.alarm.isOn",
    "vehicle.vehicle.antiTheftAlarmSystem.alarm.armStatus",
    # Range and energy
    "vehicle.drivetrain.lastRemainingRange",
    "vehicle.drivetrain.totalRemainingRange",
    "vehicle.drivetrain.electricEngine.remainingElectricRange",
    "vehicle.drivetrain.electricEngine.kombiRemainingElectricRange",
    "vehicle.drivetrain.fuelSystem.level",
    "vehicle.drivetrain.fuelSystem.remainingFuel",
    "vehicle.electricalSystem.battery.voltage",
    "vehicle.electricalSystem.battery.stateOfCharge",
    "vehicle.electricalSystem.battery.stateOfChargePlausibility",
    "vehicle.electricalSystem.battery.serviceDemand.replace",
    "vehicle.electricalSystem.battery.serviceDemand.recharge",
    # Current high-voltage battery state of charge
    "vehicle.drivetrain.batteryManagement.header",
    "vehicle.drivetrain.electricEngine.charging.acAmpere",
    "vehicle.drivetrain.electricEngine.charging.acVoltage",
    "vehicle.powertrain.electric.battery.preconditioning.automaticMode.statusFeedback",
    "vehicle.vehicle.avgAuxPower",
    "vehicle.powertrain.tractionBattery.charging.port.anyPosition.flap.isOpen",
    "vehicle.powertrain.tractionBattery.charging.port.anyPosition.isPlugged",
    "vehicle.drivetrain.electricEngine.charging.timeToFullyCharged",
    "vehicle.powertrain.electric.battery.charging.acLimit.selected",
    "vehicle.drivetrain.electricEngine.charging.method",
    "vehicle.drivetrain.electricEngine.charging.profile.mode",
    "vehicle.drivetrain.electricEngine.charging.profile.preference",
    "vehicle.drivetrain.electricEngine.charging.profile.timerType",
    "vehicle.drivetrain.electricEngine.charging.windowSelection",
    "vehicle.drivetrain.electricEngine.charging.isImmediateChargingSystemReason",
    "vehicle.drivetrain.electricEngine.charging.isSingleImmediateCharging",
    "vehicle.drivetrain.electricEngine.charging.hvpmFinishReason",
    "vehicle.body.chargingPort.plugEventId",
    "vehicle.body.chargingPort.combinedStatus",
    "vehicle.body.chargingPort.statusClearText",
    "vehicle.body.chargingPort.isoSessionId",
    "vehicle.body.chargingPort.isHospitalityActive",
    "vehicle.drivetrain.electricEngine.charging.phaseNumber",
    "vehicle.trip.segment.end.drivetrain.batteryManagement.hvSoc",
    "vehicle.trip.segment.accumulated.drivetrain.electricEngine.recuperationTotal",
    "vehicle.drivetrain.electricEngine.remainingElectricRange",
    "vehicle.drivetrain.electricEngine.charging.timeRemaining",
    "vehicle.drivetrain.electricEngine.charging.hvStatus",
    "vehicle.drivetrain.electricEngine.charging.lastChargingReason",
    "vehicle.drivetrain.electricEngine.charging.lastChargingResult",
    "vehicle.powertrain.electric.battery.preconditioning.manualMode.statusFeedback",
    "vehicle.drivetrain.electricEngine.charging.reasonChargingEnd",
    "vehicle.powertrain.electric.battery.stateOfCharge.target",
    "vehicle.powertrain.electric.battery.charging.acLimit.isActive",
    "vehicle.powertrain.electric.battery.charging.acLimit.max",
    "vehicle.powertrain.electric.battery.charging.acLimit.min",
    "vehicle.powertrain.electric.battery.charging.acousticLimit",
    "vehicle.body.chargingPort.lockedStatus",
    "vehicle.body.flap.isLocked",
    "vehicle.body.flap.isPermanentlyUnlocked",
    "vehicle.drivetrain.electricEngine.charging.level",
    "vehicle.powertrain.electric.battery.stateOfHealth.displayed",
    "vehicle.drivetrain.batteryManagement.batterySizeMax",
    "vehicle.drivetrain.batteryManagement.maxEnergy",
    "vehicle.powertrain.electric.battery.charging.power",
    "vehicle.drivetrain.electricEngine.charging.status",
    "vehicle.drivetrain.electricEngine.charging.consumptionOverLifeTime.overall.gridEnergy",
    "vehicle.drivetrain.electricEngine.charging.consumptionOverLifeTime.engineOn.gridEnergy",
    "vehicle.drivetrain.electricEngine.charging.consumptionOverLifeTime.engineOff.gridEnergy",
    "vehicle.drivetrain.electricEngine.charging.consumptionOverLifeTime.overall.referenceDistance",
    "vehicle.drivetrain.electricEngine.charging.consumptionOverLifeTime.engineOn.referenceDistance",
    "vehicle.drivetrain.electricEngine.charging.consumptionOverLifeTime.engineOff.referenceDistance",
    "vehicle.drivetrain.fuelSystem.consumptionOverLifeTime.overall.fuel",
    "vehicle.drivetrain.fuelSystem.consumptionOverLifeTime.overall.referenceDistance",
    "vehicle.drivetrain.fuelSystem.consumptionOverLifeTime.inChargeIncreasing.fuel",
    "vehicle.drivetrain.fuelSystem.consumptionOverLifeTime.inChargeIncreasing.referenceDistance",
    "vehicle.drivetrain.fuelSystem.consumptionOverLifeTime.inChargeDepleting.fuel",
    "vehicle.drivetrain.fuelSystem.consumptionOverLifeTime.inChargeDepleting.referenceDistanceEngineOn",
    "vehicle.drivetrain.fuelSystem.consumptionOverLifeTime.inChargeDepleting.referenceDistanceEngineOff",
    # HVAC / preconditioning
    "vehicle.vehicle.preConditioning.activity",
    "vehicle.vehicle.preConditioning.remainingTime",
    "vehicle.vehicle.preConditioning.error",
    "vehicle.vehicle.preConditioning.isRemoteEngineRunning",
    "vehicle.cabin.hvac.preconditioning.status.progress",
    "vehicle.cabin.hvac.preconditioning.status.remainingRunningTime",
    "vehicle.cabin.hvac.preconditioning.status.rearDefrostActive",
    "vehicle.cabin.hvac.preconditioning.configuration.defaultSettings.targetTemperature",
    "vehicle.cabin.hvac.preconditioning.configuration.directStartSettings.targetTemperature",
    "vehicle.cabin.hvac.preconditioning.configuration.isRemoteEngineStartDisclaimer",
    "vehicle.cabin.steeringWheel.heating",
    "vehicle.cabin.hvac.preconditioning.configuration.defaultSettings.steeringWheel.heating",
    "vehicle.cabin.hvac.preconditioning.configuration.directStartSettings.steeringWheel.heating",
    "vehicle.cabin.climate.timers.overwriteTimer.action",
    "vehicle.cabin.climate.timers.overwriteTimer.hour",
    "vehicle.cabin.climate.timers.overwriteTimer.minute",
    "vehicle.cabin.climate.timers.weekdaysTimer1.action",
    "vehicle.cabin.climate.timers.weekdaysTimer1.hour",
    "vehicle.cabin.climate.timers.weekdaysTimer1.minute",
    "vehicle.cabin.climate.timers.weekdaysTimer2.action",
    "vehicle.cabin.climate.timers.weekdaysTimer2.hour",
    "vehicle.cabin.climate.timers.weekdaysTimer2.minute",
    # Trip summary
    "vehicle.trip.segment.end.time",
    "vehicle.trip.segment.end.travelledDistance",
    "vehicle.trip.segment.accumulated.acceleration.starsAverage",
    "vehicle.trip.segment.accumulated.chassis.brake.starsAverage",
    "vehicle.trip.segment.accumulated.drivetrain.electricEngine.energyConsumptionComfort",
    "vehicle.trip.segment.accumulated.drivetrain.transmission.setting.fractionDriveElectric",
    "vehicle.trip.segment.accumulated.drivetrain.transmission.setting.fractionDriveEcoPro",
    # Service / tyres
    "vehicle.chassis.axle.wheel.tire.diagnosis",
    "vehicle.chassis.axle.row1.wheel.left.tire.temperature",
    "vehicle.chassis.axle.row1.wheel.right.tire.temperature",
    "vehicle.chassis.axle.row2.wheel.left.tire.temperature",
    "vehicle.chassis.axle.row2.wheel.right.tire.temperature",
    "vehicle.status.checkControlMessages",
    "vehicle.status.conditionBasedServices",
    "vehicle.status.conditionBasedServicesCount",
    "vehicle.status.conditionBasedServicesAverageDistancePerDay",
    "vehicle.status.serviceDistance.next",
    "vehicle.status.serviceDistance.yellow",
    "vehicle.status.serviceTime.inspectionDateLegal",
    "vehicle.status.serviceTime.yellow",
    "vehicle.status.serviceTime.hUandAuServiceYellow",
    "vehicle.channel.teleservice.status",
    "vehicle.channel.teleservice.lastAutomaticServiceCallTime",
    "vehicle.channel.teleservice.lastTeleserviceReportTime",
    "vehicle.channel.teleservice.lastBreakdownCallTime",
    "vehicle.channel.teleservice.lastManualCallTime",
    "vehicle.electronicControlUnit.diagnosticTroubleCodes.raw",
    "vehicle.serviceDemand.defect.id",
    "vehicle.sevice.preferredSevicePartner",
]

#fetch_vehicle_mapping returns data like this:
#2025-09-29 18:11:26.340 INFO (MainThread) [custom_components.cardata] Cardata vehicle mappings: [{'mappedSince': '2025-03-27T17:48:41.435Z', 'mappingType': 'PRIMARY', 'vin': 'WBY31AW090FP15359'}, {'mappedSince': '2023-10-10T13:29:38.484Z', 'mappingType': 'PRIMARY', 'vin': 'WBY1Z21020V791850'}]

#telematic reqeusts returns data like this:
#2025-09-29 19:48:19.076 INFO (MainThread) [custom_components.cardata] Cardata telematic data for WBY31AW090FP15359: {'telematicData': {'vehicle.powertrain.electric.battery.preconditioning.manualMode.statusFeedback': {'timestamp': None, 'unit': None, 'value': None}, 'vehicle.powertrain.tractionBattery.charging.port.anyPosition.isPlugged': {'timestamp': None, 'unit': None, 'value': None}, 'vehicle.powertrain.electric.battery.stateOfHealth.displayed': {'timestamp': None, 'unit': None, 'value': None}, 'vehicle.drivetrain.electricEngine.remainingElectricRange': {'timestamp': '2025-09-29T16:48:19.019Z', 'unit': 'km', 'value': '286'}, 'vehicle.powertrain.electric.battery.stateOfCharge.target': {'timestamp': '2025-09-29T13:21:16.000Z', 'unit': '%', 'value': '85'}, 'vehicle.trip.segment.end.drivetrain.batteryManagement.hvSoc': {'timestamp': '2025-09-29T12:15:55.055Z', 'unit': '%', 'value': '74'}, 'vehicle.drivetrain.electricEngine.charging.lastChargingResult': {'timestamp': '2025-09-29T16:48:19.019Z', 'unit': None, 'value': 'FAILED'}, 'vehicle.powertrain.electric.battery.charging.acLimit.selected': {'timestamp': '2025-09-29T13:21:16.000Z', 'unit': 'A', 'value': '8'}, 'vehicle.drivetrain.electricEngine.charging.phaseNumber': {'timestamp': None, 'unit': None, 'value': None}, 'vehicle.drivetrain.batteryManagement.batterySizeMax': {'timestamp': '2025-09-29T13:21:16.000Z', 'unit': 'kWh', 'value': '0'}, 'vehicle.drivetrain.electricEngine.charging.method': {'timestamp': '2025-09-29T13:21:16.000Z', 'unit': None, 'value': 'NOCHARGING'}, 'vehicle.body.chargingPort.lockedStatus': {'timestamp': '2025-09-29T13:21:16.000Z', 'unit': None, 'value': 'CHARGING_CABLE_NOT_LOCKED'}, 'vehicle.powertrain.tractionBattery.charging.port.anyPosition.flap.isOpen': {'timestamp': None, 'unit': None, 'value': None}, 'vehicle.vehicle.avgAuxPower': {'timestamp': '2025-09-29T13:21:16.000Z', 'unit': 'kW', 'value': '0.5'}, 'vehicle.body.chargingPort.plugEventId': {'timestamp': '2025-09-29T13:21:16.000Z', 'unit': None, 'value': '1133'}, 'vehicle.drivetrain.electricEngine.charging.timeToFullyCharged': {'timestamp': None, 'unit': 'min', 'value': None}, 'vehicle.drivetrain.electricEngine.charging.lastChargingReason': {'timestamp': '2025-09-29T16:48:19.019Z', 'unit': None, 'value': 'INVALID'}, 'vehicle.trip.segment.accumulated.drivetrain.electricEngine.recuperationTotal': {'timestamp': None, 'unit': None, 'value': None}, 'vehicle.drivetrain.electricEngine.charging.hvStatus': {'timestamp': '2025-09-29T16:48:19.019Z', 'unit': None, 'value': 'NOT_CHARGING'}, 'vehicle.drivetrain.electricEngine.charging.reasonChargingEnd': {'timestamp': None, 'unit': None, 'value': None}, 'vehicle.drivetrain.electricEngine.charging.acVoltage': {'timestamp': None, 'unit': 'V', 'value': None}, 'vehicle.drivetrain.electricEngine.charging.acAmpere': {'timestamp': None, 'unit': 'A', 'value': None}, 'vehicle.drivetrain.electricEngine.charging.level': {'timestamp': '2025-09-29T16:48:19.019Z', 'unit': '%', 'value': '74'}, 'vehicle.powertrain.electric.battery.preconditioning.automaticMode.statusFeedback': {'timestamp': None, 'unit': None, 'value': None}, 'vehicle.drivetrain.electricEngine.charging.timeRemaining': {'timestamp': None, 'unit': 'min', 'value': None}, 'vehicle.drivetrain.batteryManagement.header': {'timestamp': '2025-09-29T13:21:16.000Z', 'unit': '%', 'value': '74'}, 'vehicle.vehicleIdentification.basicVehicleData': {'timestamp': None, 'unit': None, 'value': None}}}

#vehicle basic data response:
#2025-09-29 20:05:01.272 INFO (MainThread) [custom_components.cardata] Cardata basic data for WBY31AW090FP15359: {'bodyType': 'Coupe', 'brand': 'BMW', 'chargingModes': ['AC_LOW'], 'colourCodeRaw': 'C57', 'colourDescription': 'AVENTURINROT III METALLIC', 'constructionDate': '2022-11-24T00:00:00.000+0000', 'countryCode': 'FI', 'driveTrain': 'BEV', 'engine': 'XE2', 'fullSAList': '02PA,02VF,08TR,01CB,0487,0230,02VB,0420,0754,0775,0403,0654,06AF,02NH,02VL,0428,04V1,0322,08TF,04AW,04T2,04UR,08R9,06NX,0430,0493,06U3,08WQ,0688,0459,03AC,0854,01CX,04U9,0491,05AZ,0548,0715,02VC,04LN,05DN,06AE,05AC,04T3,0534,0881,0302,06C4,05AQ,0494,05AU,0431,0760,03FP,07M9,08WH,06AK,06VB,05DA', 'hasNavi': True, 'hasSunRoof': True, 'headUnit': 'HU_MGU', 'modelKey': '31AW', 'modelName': 'i4 M50', 'numberOfDoors': 5, 'propulsionType': 'EL', 'series': '4', 'seriesDevt': 'G26', 'simStatus': 'ACTIVE', 'steering': 'LL'}
