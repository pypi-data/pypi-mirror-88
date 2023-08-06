#include "bindings.h"

#pragma once

#if defined(ON_PYTHON_COMPILE)
void initTextureBindings(pybind11::module& m);
#else
void initTextureBindings(void* m);
#endif

class BND_Texture : public BND_CommonObject
{
public:
  ON_Texture* m_texture = nullptr;
public:
  BND_Texture();
  BND_Texture(ON_Texture* texture, const ON_ModelComponentReference* compref);

  std::wstring GetFileName() const { return std::wstring(m_texture->m_image_file_reference.FullPathAsPointer()); }
  void SetFileName(std::wstring path) { m_texture->m_image_file_reference.SetFullPath(path.c_str(), true); }
  class BND_FileReference* GetFileReference() const;
  //public Guid Id
  //public bool Enabled
  //public TextureType TextureType
  //public int MappingChannelId
  //public TextureCombineMode TextureCombineMode
  //public TextureUvwWrapping WrapU
  //public TextureUvwWrapping WrapV
  //public TextureUvwWrapping WrapW
  //public Transform UvwTransform
  //public void GetAlphaBlendValues(out double constant, out double a0, out double a1, out double a2, out double a3)
  //public void SetAlphaBlendValues(double constant, double a0, double a1, double a2, double a3)
  //public void SetRGBBlendValues(Color color, double a0, double a1, double a2, double a3)

protected:
  void SetTrackedPointer(ON_Texture* texture, const ON_ModelComponentReference* compref);
};