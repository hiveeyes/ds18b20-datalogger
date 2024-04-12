![Alt-Text](https://community.hiveeyes.org/uploads/default/optimized/2X/f/f59f0149306b811f793627ec956c3e43c3758e51_2_334x500.jpeg)

# temp-matrix
temperature matrix based on raspberry pi, python, 5x6 ds18b20, and grafana

for development details see: [https://community.hiveeyes.org/t/laborprotokoll-4x5-temp-matrix-mit-ds18b20/5102/14](URL)

## files
  * README.md - this file
  * LICENSE
  * temp-matrix_5x6.py - sensor reading and data logging to hiveeyes
  * temp-matrix_5x6-grafana_desktop.json - description of [grafana desktop](https://swarm.hiveeyes.org/grafana/d/T49wHSaIk/mois-ex-wtf-test-ds18b20-5x6-temp-matrix-svg-pixmap?orgId=2&from=1712771622514&to=1712807415379)

## sensor wiring
be aware that you might have to ajust your resistors size.
with 30 sensors i had erratic sensor mapping using a 4.7k resistor.
i am getting valid mapping using a 2.2k resistor.

## sensor mapping
[https://community.hiveeyes.org/t/ds18b20-temperatur-sensoren-am-one-wire-bus-anordnen/1399
](URL)

## data publishing
paho-mqtt required: [https://pypi.org/project/paho-mqtt/#installation](URL)

    ssh youruser@yourpi
    screen
    cd temp-matrix
    source paho-mqtt/bin/activate
    python temp-matrix_5x6.py`

### mqtt data upload to hiveeyes
[https://community.hiveeyes.org/t/daten-per-mqtt-und-python-ans-backend-auf-swarm-hiveeyes-org-ubertragen/94/6](URL)

### format your array
[https://community.hiveeyes.org/t/how-to-visualize-2-dimensional-temperature-data-in-grafana/974/9
](URL)

     matrix = [[temp_ir_1_1, temp_ir_1_2, temp_ir_1_3, temp_ir_1_4, temp_ir_1_5, temp_ir_1_6], \
          [temp_ir_2_1, temp_ir_2_2, temp_ir_2_3, temp_ir_2_4, temp_ir_2_5, temp_ir_2_6], \
          [temp_ir_3_1, temp_ir_3_2, temp_ir_3_3, temp_ir_3_4, temp_ir_3_5, temp_ir_3_6], \
          [temp_ir_4_1, temp_ir_4_2, temp_ir_4_3, temp_ir_4_4, temp_ir_4_5, temp_ir_4_6], \
          [temp_ir_5_1, temp_ir_5_2, temp_ir_5_3, temp_ir_5_4, temp_ir_5_5, temp_ir_5_6]]

## data visualizing (grafana)
[https://swarm.hiveeyes.org/grafana/d/Y9PcgE4Sz/mois-ex-wtf-test-ir-sensor-svg-pixmap-copy
](URL)

## bonus: sensors offsets
[https://community.hiveeyes.org/t/temperatursensoren-justieren-kalibrieren/1744/2
](URL)






