#!/usr/bin/python
import os
import cv2


class Generator:
        def __init__(self):
                with open('template/model.sdf', 'r') as f:
                        self.sdf_template = f.read()

                with open('template/model.config', 'r') as f:
                        self.config_template = f.read()

                with open('template/materials/scripts/Apriltag.material', 'r') as f:
                        self.material_template = f.read()

        def generate(self, tag_directory, original_name, tag_name, tag_size, tag_size_m, tag_thickness):
                img = cv2.imread('%s/%s.png' % (tag_directory, original_name), 0)
                img = cv2.resize(img, (tag_size, tag_size), interpolation=cv2.INTER_NEAREST)


                if not os.path.exists('models/April%s/materials/scripts' % tag_name):
                        os.makedirs('models/April%s/materials/scripts' % tag_name)

                if not os.path.exists('models/April%s/materials/textures' % tag_name):
                        os.makedirs('models/April%s/materials/textures' % tag_name)

                with open('models/April%s/model.sdf' % tag_name, 'w') as f:
                    buf = self.sdf_template
                    buf = buf.replace('tag36_11_00000', tag_name)
                    buf = buf.replace("tag_size", str(tag_size_m))
                    buf = buf.replace("tag_thickness", str(tag_thickness))
                    f.write(buf)

                with open('models/April%s/model.config' % tag_name, 'w') as f:
                        f.write(self.config_template.replace('tag36_11_00000', tag_name))

                with open('models/April%s/materials/scripts/Apriltag.material' % tag_name, 'w') as f:
                        f.write(self.material_template.replace('tag36_11_00000', tag_name))

                cv2.imwrite('models/April%s/materials/textures/%s.png' % (tag_name, tag_name), img)


def main():
        # Texture size must be power of two
        # With the default tag image size (10pix), tags will not be clearly rendered due to rescaling and interpolation
        tag_size = 1024

        generator = Generator()
        for i in range(5):
                generator.generate('apriltag-imgs/tagStandard41h12', 'tag41_12_%05d' % i, 'tag41_12_7cm_%05d' % i, tag_size, 0.07, 0.01)


if __name__ == '__main__':
        main()
