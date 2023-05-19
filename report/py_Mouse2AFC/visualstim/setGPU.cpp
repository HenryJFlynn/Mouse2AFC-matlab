// C:\Users\hatem\OneDrive\Documents\BpodUser\Protocols\Mouse2AFC\report\py_Mouse2AFC\visualstim>cl /LD setGPU.cpp

#ifdef _WIN32
#include <windows.h>

typedef struct _GPU_DEVICE {
    DWORD cb;
    CHAR DeviceName[32];
    CHAR DeviceString[128];
    DWORD Flags;
    RECT rcVirtualScreen; } GPU_DEVICE, *PGPU_DEVICE;

DECLARE_HANDLE(HGPUNV);
extern "C" {
    // _declspec(dllexport) GPU_DEVICE GPU_DEVICE_;
    // _declspec(dllexport) PGPU_DEVICE PGPU_DEVICE_;
    _declspec(dllexport) int WGL_ERROR_INCOMPATIBLE_AFFINITY_MASKS_NV =  0x20D0;
	_declspec(dllexport) int WGL_ERROR_MISSING_AFFINITY_MASK_NV = 0x20D1;
    _declspec(dllexport) int AmdPowerXpressRequestHighPerformance = 1;
	// _declspec(dllexport) BOOL wglEnumGpusNV (UINT iGpuIndex, HGPUNV *phGpu);
	// _declspec(dllexport) BOOL wglEnumGpuDevicesNV (HGPUNV hGpu, UINT iDeviceIndex, PGPU_DEVICE lpGpuDevice);
	// _declspec(dllexport) HDC wglCreateAffinityDCNV (const HGPUNV *phGpuList);
	// _declspec(dllexport) BOOL wglEnumGpusFromAffinityDCNV (HDC hAffinityDC, UINT iGpuIndex, HGPUNV *hGpu);
	// _declspec(dllexport) BOOL wglDeleteDCNV (HDC hdc);
    _declspec(dllexport) DWORD NvOptimusEnablement = 0x00000001;
    _declspec(dllexport) int WGL_NV_gpu_affinity = 1;
}
#endif
