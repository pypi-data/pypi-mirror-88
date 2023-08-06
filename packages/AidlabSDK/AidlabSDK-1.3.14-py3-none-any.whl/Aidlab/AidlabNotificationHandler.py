#
# AidlabNotificationHandler.py
# Aidlab-SDK
# Created by Szymon Gesicki on 09.05.2020.
#

from Aidlab.AidlabCharacteristicsUUID import AidlabCharacteristicsUUID

class AidlabNotificationHandler(object):


    def __init__(self, aidlab_address, delegate):
        self.aidlab_address = aidlab_address
        self.delegate = delegate

    def handle_notification(self, sender, data):

        if sender == AidlabCharacteristicsUUID.temperatureUUID["handle"] or sender.upper() == AidlabCharacteristicsUUID.temperatureUUID["uuid"].upper():
            self.delegate.did_receive_raw_temperature(data, self.aidlab_address)

        elif sender == AidlabCharacteristicsUUID.ecgUUID["handle"] or sender.upper() == AidlabCharacteristicsUUID.ecgUUID["uuid"].upper():
            self.delegate.did_receive_raw_ecg(data, self.aidlab_address)

        elif sender == AidlabCharacteristicsUUID.batteryUUID["handle"] or sender.upper() == AidlabCharacteristicsUUID.batteryUUID["uuid"].upper():
            self.delegate.did_receive_raw_battery_level(data, self.aidlab_address)

        elif sender == AidlabCharacteristicsUUID.respirationUUID["handle"] or sender.upper() == AidlabCharacteristicsUUID.respirationUUID["uuid"].upper():
            self.delegate.did_receive_raw_respiration(data, self.aidlab_address)

        elif sender == AidlabCharacteristicsUUID.motionUUID["handle"] or sender.upper() == AidlabCharacteristicsUUID.motionUUID["uuid"].upper():
            self.delegate.did_receive_raw_imu_values(data, self.aidlab_address)

        elif sender == AidlabCharacteristicsUUID.activityUUID["handle"] or sender.upper() == AidlabCharacteristicsUUID.activityUUID["uuid"].upper():
            self.delegate.did_receive_raw_activity(data, self.aidlab_address)

        elif sender == AidlabCharacteristicsUUID.stepsUUID["handle"] or sender.upper() == AidlabCharacteristicsUUID.stepsUUID["uuid"].upper():
            self.delegate.did_receive_raw_steps(data, self.aidlab_address)

        elif sender == AidlabCharacteristicsUUID.orientationUUID["handle"] or sender.upper() == AidlabCharacteristicsUUID.orientationUUID["uuid"].upper():
            self.delegate.did_receive_raw_orientation(data, self.aidlab_address)

        elif sender == AidlabCharacteristicsUUID.heartRateUUID["handle"] or sender.upper() == AidlabCharacteristicsUUID.heartRateUUID["uuid"].upper() or sender.upper() == "2A37":
            self.delegate.did_receive_raw_heart_rate(data, self.aidlab_address)

        elif sender == AidlabCharacteristicsUUID.healthThermometerUUID["handle"] or sender.upper() == AidlabCharacteristicsUUID.healthThermometerUUID["uuid"].upper() or sender.upper() == "2A1C":
            self.delegate.did_receive_raw_health_thermometer(data, self.aidlab_address)

        elif sender == AidlabCharacteristicsUUID.soundVolumeUUID["handle"] or sender.upper() == AidlabCharacteristicsUUID.soundVolumeUUID["uuid"].upper():
            self.delegate.did_receive_raw_sound_volume(data, self.aidlab_address)

        elif sender == AidlabCharacteristicsUUID.cmdUUID["handle"] or sender.upper() == AidlabCharacteristicsUUID.cmdUUID["uuid"].upper():
            self.delegate.did_receive_raw_cmd_value(data, self.aidlab_address)

    