#include "Sodaq_wdt.h"

void initWdt();

void systemSleep(bool isDeepSleep);

void longSleep(unsigned long sleepTimeMilliSec, bool isDeepSleep);
