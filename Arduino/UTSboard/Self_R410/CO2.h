#include <stdint.h>

uint16_t _generate_crc(uint8_t pdu[], int len);

int _handler(uint8_t pdu[], uint8_t funCode, int len);

int modbus_read_response(int waitBytes, uint8_t funCode);

int read_device_id(uint8_t comAddr, uint8_t objId);

void read_sensor_id(uint8_t target);

int read_input_registers(uint8_t comAddr, uint16_t regAddr, uint16_t numReg);

uint16_t read_sensor_measurements();