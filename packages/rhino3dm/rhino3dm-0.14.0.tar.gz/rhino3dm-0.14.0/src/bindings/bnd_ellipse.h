#include "bindings.h"

#pragma once

#if defined(ON_PYTHON_COMPILE)
void initEllipseBindings(pybind11::module& m);
#else
void initEllipseBindings(void* m);
#endif

class BND_Ellipse
{
public:
  ON_Ellipse m_ellipse;
public:
  //public Ellipse(Plane plane, double radius1, double radius2)
  //public Ellipse(Point3d center, Point3d second, Point3d third)
  //public Plane Plane | get; set;
  //public double Radius1 | get; set;
  //public double Radius2 | get; set;
  bool IsValid() const { return m_ellipse.IsValid(); }
  //public NurbsCurve ToNurbsCurve()
  //public bool EpsilonEquals(Ellipse other, double epsilon)
};
