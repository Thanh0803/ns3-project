
#ifdef NS3_MODULE_COMPILATION
# error "Do not include ns3 module aggregator headers from other modules; these are meant only for end user scripts."
#endif

#ifndef NS3_MODULE_SIMPLE_WIRELESS
    

// Module headers:
#include "drop-head-queue.h"
#include "simple-wireless-channel.h"
#include "simple-wireless-net-device.h"
#include "snr-per-error-model.h"
#include "two-state-propagation-loss-model.h"
#endif
