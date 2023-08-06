#include <Zivid/Calibration/Detector.h>

#include <ZividPython/Calibration/Detector.h>

#include <pybind11/pybind11.h>

namespace py = pybind11;

namespace ZividPython
{
    void wrapClass(pybind11::class_<Zivid::Calibration::DetectionResult> pyClass)
    {
        pyClass.def("valid", &Zivid::Calibration::DetectionResult::valid);
    }
} // namespace ZividPython
