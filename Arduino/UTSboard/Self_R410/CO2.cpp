#include "CO2.h"
#include <Arduino.h>
#include <stdint.h>
const uint8_t SUNRISE_ADDR = 0x68;
const int WAIT_MS = 180;
const int INTER_PACKET_INTERVAL_MS = 4;
const int COMMUNICATION_ERROR = -1;
const int ILLEGAL_FUNCTION = 1;
const int ILLEGAL_DATA_ADDRESS = 2;
const int ILLEGAL_DATA_VALUE = 3;
const uint16_t ERROR_STATUS = 0x0003;
const uint16_t MEASUREMENT_MODE = 0x000A;
const uint16_t CONTINUOUS = 0x0000;
const uint16_t SINGLE = 0x0001;
int readPeriodMs = 4000;
uint8_t request[256];
uint8_t response[256];
uint16_t values[256];
char device[12];

#define DEBUG_STREAM SerialUSB

uint16_t _generate_crc(uint8_t pdu[], int len) {
  uint16_t crc = 0xFFFF;

  for (int pos = 0; pos < len; pos++) {
    /* XOR the byte into the least significant byte of crc */
    crc ^= (uint16_t)pdu[pos];

    /* Loop through the entire message */
    for (int n = 8; n != 0; n--) {
      /* If the LSB is 1, shift right and XOR 0xA001 */
      /* Otherwise, just shift right */
      if ((crc & 0x0001) != 0) {
        crc >>= 1;
        crc ^= 0xA001;

      } else {
        crc >>= 1;
      }
    }
  }
  return crc;
}
int _handler(uint8_t pdu[], uint8_t funCode, int len) {
  /* Return variable */
  int error = 0;
  /* Function variables */
  uint8_t exceptionFunCode = funCode + 0x80;
  /* Check for malformed packet */
  if (len >= 4) {
    /* Check for corrupt data in the response */
    uint16_t crc = _generate_crc(pdu, (len - 2));
    uint8_t crcHi = (crc >> 8);
    uint8_t crcLo = crc & 0xFF;

    if (crcLo != pdu[len - 2] || crcHi != pdu[len - 1]) {
         DEBUG_STREAM.println("_handler comm error pdu");
      return COMMUNICATION_ERROR;
    }

    /* Check response for exceptions */
    if (pdu[1] == exceptionFunCode) {
      switch (pdu[2]) {
      case ILLEGAL_FUNCTION:
         DEBUG_STREAM.println("_handler illegal function");
        error = -ILLEGAL_FUNCTION;
        break;

      case ILLEGAL_DATA_ADDRESS:
        error = -ILLEGAL_DATA_ADDRESS;
        break;

      case ILLEGAL_DATA_VALUE:
        error = -ILLEGAL_DATA_VALUE;
        break;

      default:
         DEBUG_STREAM.println("_handler comm error switch");
        error = COMMUNICATION_ERROR;
        break;
      }
    }
  } else {
     DEBUG_STREAM.println("_handler comm error");
    error = COMMUNICATION_ERROR;
  }
  return error;
}
int modbus_read_response(int waitBytes, uint8_t funCode) {
  /* Time-out variable */
  unsigned long byteTime = millis();
  int available_bytes;
  unsigned long timestamp;
  /* Return variable */
  int error;

  /* Wait for first byte in packet */
  while ((available_bytes = Serial.available()) == 0) {
    unsigned long timeout = (unsigned long)((long)millis() - (long)byteTime);
    if (WAIT_MS < timeout) {
         DEBUG_STREAM.println("Here");
      return COMMUNICATION_ERROR;
    }
  }
//     DEBUG_STREAM.println("After Here");

  byteTime = millis();

  do {
    int new_available_bytes = Serial.available();

    timestamp = millis();

    if (available_bytes != new_available_bytes) {
      byteTime = timestamp;
      available_bytes = new_available_bytes;
    }
  } while (INTER_PACKET_INTERVAL_MS >
           (unsigned long)((long)timestamp - (long)byteTime));

  for (int n = 0; n < available_bytes; n++) {
    response[n] = Serial.read();
  }

  /* Check response for exceptions */
  error = _handler(response, funCode, available_bytes);

  return ((error == 0) ? available_bytes : error);
}
int read_device_id(uint8_t comAddr, uint8_t objId) {
  /* Return variable */
  int error = 0;
  /* PDU variables */
  uint8_t funCode = 0x2B;
  uint8_t meiType = 0x0E;
  uint8_t idCode = 0x04;

  /* Define Modbus PDU */
  request[0] = comAddr;
  request[1] = funCode;
  request[2] = meiType;
  request[3] = idCode;
  request[4] = objId;

  /* Create CRC */
  uint16_t crc = _generate_crc(request, 5);
  uint8_t crcLo = crc & 0xFF;
  uint8_t crcHi = (crc >> 8);

  request[5] = crcLo;
  request[6] = crcHi;

  /* Send request */
  Serial.write(request, 7);

  /* Number of bytes to wait for */
  int objLen = 0;
  if (objId == 0) {
    objLen = 8;
  } else if (objId == 1) {
    objLen = 7;
  } else if (objId == 2) {
    objLen = 4;
  }
  int waitBytes = 12 + objLen;
  /* Wait for response */
  error = modbus_read_response(waitBytes, funCode);
  if (error > 0) {
    /* Combine the bytes containing the requested values into words */
    int objLength = response[9];
    int slot = 10;
    for (int n = 0; n < objLength; n++) {
      device[n] = response[slot];

      slot++;
    }
    device[objLength] = '\0';
    return 0;
  } else {
    return error;
  }
}
void read_sensor_id(uint8_t target) {
  /* Vendor Name */
  if (read_device_id(target, 0) != 0) {
    // DEBUG_STREAM.println("EXCEPTION: Failed to read Vendor Name");
  } else {
    // DEBUG_STREAM.print("Vendor Name: ");
    // DEBUG_STREAM.println(device);
  }

  /* ProductCode */
  if (read_device_id(target, 1) != 0) {
    // DEBUG_STREAM.println("EXCEPTION: Failed to read ProductCode");
  } else {
    // DEBUG_STREAM.print("ProductCode: ");
    // DEBUG_STREAM.println(device);
  }

  /* MajorMinorRevision */
  if (read_device_id(target, 2) != 0) {
    // DEBUG_STREAM.println("EXCEPTION: Failed to read MajorMinorRevision");
  } else {
    // DEBUG_STREAM.print("MajorMinorRevision: ");
    // DEBUG_STREAM.println(device);
  }
}
int read_input_registers(uint8_t comAddr, uint16_t regAddr, uint16_t numReg) {
  /* Return variable */
  int error = 0;
  /* PDU variables */
  uint8_t funCode = 0x04;

  uint8_t regAddrHi = (regAddr >> 8);
  uint8_t regAddrLo = regAddr & 0xFF;

  uint8_t numRegHi = (numReg >> 8);
  uint8_t numRegLo = numReg & 0xFF;

  /* Define Modbus PDU */
  request[0] = comAddr;
  request[1] = funCode;
  request[2] = regAddrHi;
  request[3] = regAddrLo;
  request[4] = numRegHi;
  request[5] = numRegLo;

  /* Create CRC */
  uint16_t crc = _generate_crc(request, 6);
  uint8_t crcLo = crc & 0xFF;
  uint8_t crcHi = (crc >> 8);

  request[6] = crcLo;
  request[7] = crcHi;

  /* Send request */
  Serial.write(request, 8);

  /* Number of bytes to wait for */
  int waitBytes = 5 + (numReg * 2);
  /* Wait for response */
  error = modbus_read_response(waitBytes, funCode);

//  DEBUG_STREAM.print("After modbus_read_response: ");
//  DEBUG_STREAM.println(error);

  /* If no error were encountered, combine the bytes containing the requested
   * values into words */
  if (error > 0) {
    int counter = 0;
    int slot = 3;
    while (counter < ((error - 5) / 2)) {
      values[counter] =
          ((int16_t)(int8_t)response[slot] << 8) | (uint16_t)response[slot + 1];

      counter++;
      slot = slot + 2;
    }
  } else {
    return error;
  }

  return 0;
}
uint16_t read_sensor_measurements() {
  const uint8_t target = SUNRISE_ADDR;
  /* Function variables */
  int error;
  uint16_t numReg = 0x0001;

  /* Read values */
  if ((error = read_input_registers(target, ERROR_STATUS, numReg)) != 0) {
    // DEBUG_STREAM.print("EXCEPTION! Failed to read input registers. Error
    // code: "); 
//    DEBUG_STREAM.println(error);
  } else {
    /* Read CO2 concentration */
//     DEBUG_STREAM.print("CO2: ");
     DEBUG_STREAM.print(values[0]);
     DEBUG_STREAM.println(" ppm");
    /* Read error status */
//     DEBUG_STREAM.print("Error Status: 0x");
//     DEBUG_STREAM.println(values[0], HEX);
  }
  return values[0];
}
