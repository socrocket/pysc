// vim : set fileencoding=utf-8 expandtab noai ts=4 sw=4 :
/// @addtogroup pysc
/// @{
/// @file amba.i
///
/// @date 2013-2014
/// @copyright All rights reserved.
///            Any reproduction, use, distribution or disclosure of this
///            program, without the express, prior written consent of the
///            authors is strictly prohibited.
/// @author Rolf Meyer
%module amba

%include "std_string.i"
%include "stdint.i"
%include "usi.i"

USI_REGISTER_MODULE(amba)

%{
#include "core/common/amba.h"
#include "core/common/ahbdevicebase.h"
#include "core/common/apbdevicebase.h"
#include "core/common/clkdevice.h"
%}

%include "core/common/amba.h"
%include "core/common/ahbdevicebase.h"
%include "core/common/apbdevicebase.h"
%include "core/common/clkdevice.h"

%{
USI_REGISTER_OBJECT(AHBDeviceBase);
USI_REGISTER_OBJECT(APBDeviceBase);
USI_REGISTER_OBJECT(CLKDevice);
%}
