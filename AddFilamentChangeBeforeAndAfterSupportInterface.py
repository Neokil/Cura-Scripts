#
# Cura PostProcessingPlugin
# Author:   Simon Schulte
# Date:     2024-01-15
# Modified: 2024-01-15
#
# Description:  This script looks for Support interfaces and adds a M600 filament change before and after the interface gcode.
#
from ..Script import Script
from UM.Application import Application

class AddFilamentChangeBeforeAndAfterSupportInterface(Script):
    def __init__(self):
        super().__init__()

    def getSettingDataString(self):
        return """{
            "name": "Add filament change before and after support interface",
            "key": "AddFilamentChangeBeforeAndAfterSupportInterface",
            "metadata": {},
            "version": 2,
            "settings":
            {
                "M600 Beeps":
                {
                    "label": "M600 Beeps",
                    "description": "Defines how many times the printer will beep for the filament change",
                    "type": "int",
                    "default_value": 3
                },
                "M600 X-Position":
                {
                    "label": "M600 X-Position",
                    "description": "Defines where the print head will move to for the filament change",
                    "type": "int",
                    "default_value": 100
                },
                "M600 Y-Position":
                {
                    "label": "M600 Y-Position",
                    "description": "Defines where the print head will move to for the filament change",
                    "type": "int",
                    "default_value": 0
                },
                "M600 Z-Offset":
                {
                    "label": "M600 Z-Offset",
                    "description": "Defines where the print head will move to for the filament change",
                    "type": "int",
                    "default_value": 20
                }
            }
        }"""
    
    def execute(self, data):
        beeps = self.getSettingValueByKey("M600 Beeps")
        xpos = self.getSettingValueByKey("M600 X-Position")
        ypos = self.getSettingValueByKey("M600 Y-Position")
        zoffset = self.getSettingValueByKey("M600 Z-Offset")

        for layer in data:
            layer_index = data.index(layer)
            lines = layer.split("\n")
            final_lines = []
            support_found = False
            for line in lines:
                if line.startswith(";TYPE:SUPPORT-INTERFACE"):
                    support_found = True
                    final_lines.append(line)
                    final_lines.append("M600 B{beeps} X{xpos} Y{ypos} Z{zoffset}")
                elif line.startswith(";TYPE:") and support_found:
                    support_found = False
                    final_lines.append("M600 B{beeps} X{xpos} Y{ypos} Z{zoffset}")
                    final_lines.append(line)
                else:
                    final_lines.append(line)
                    
            data[layer_index] = "\n".join(final_lines)
            
        return data