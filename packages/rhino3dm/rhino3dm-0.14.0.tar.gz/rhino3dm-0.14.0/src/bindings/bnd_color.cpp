#include "bindings.h"

#if defined(ON_PYTHON_COMPILE)

BND_Color ON_Color_to_Binding(const ON_Color& color)
{
  return pybind11::make_tuple(color.Red(), color.Green(), color.Blue(), 255 - color.Alpha());
}

ON_Color Binding_to_ON_Color(const BND_Color& color)
{
  int r = color[0].cast<int>();
  int g = color[1].cast<int>();
  int b = color[2].cast<int>();
  int a = color[3].cast<int>();
  return ON_Color(r, g, b, 255-a);
}

#endif

#if defined(ON_WASM_COMPILE)

BND_Color ON_Color_to_Binding(const ON_Color& color)
{
  emscripten::val v(emscripten::val::object());
  v.set("r", emscripten::val(color.Red()));
  v.set("g", emscripten::val(color.Green()));
  v.set("b", emscripten::val(color.Blue()));
  v.set("a", emscripten::val(255 - color.Alpha()));
  return v;
}

ON_Color Binding_to_ON_Color(const BND_Color& color)
{
  int r = color["r"].as<int>();
  int g = color["g"].as<int>();
  int b = color["b"].as<int>();
  int a = color["a"].as<int>();
  return ON_Color(r,g,b,255-a);
}
#endif
