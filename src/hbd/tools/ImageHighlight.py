from PIL import Image, ImageDraw
from utils import Log

log = Log('ImageHighlight')


class ImageHighlight:
    def __init__(
        self, original_image_path: str, guide_image_path: str, dim: int
    ):
        self.original_image_path = original_image_path
        self.guide_image_path = guide_image_path
        self.dim = dim

    @staticmethod
    def get_fp(image_path: str, dim: int):
        im = Image.open(image_path)
        fp = []
        for i in range(0, im.size[0], dim):
            fp_i = []
            for j in range(0, im.size[1], dim):
                square = im.crop((i, j, i + dim, j + dim))
                grayscale_square = square.convert("L")
                pixels = list(grayscale_square.getdata())
                avg_brightness = sum(pixels) / len(pixels)
                fp_ij = avg_brightness
                fp_i.append(fp_ij)
            fp.append(fp_i)
        return fp

    def write(self, output_image_path: str):
        fp_original = self.get_fp(self.original_image_path, self.dim)
        fp_guide = self.get_fp(self.guide_image_path, self.dim)

        im = Image.open(self.original_image_path).convert("RGBA")
        overlay = Image.new("RGBA", im.size, (255, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        for i in range(0, im.size[0], self.dim):
            for j in range(0, im.size[1], self.dim):
                ki = i // self.dim
                kj = j // self.dim
                fp_ij_original = fp_original[ki][kj]
                fp_ij_guide = fp_guide[ki][kj]

                if (fp_ij_guide - fp_ij_original) < 10:
                    continue

                top_left = (ki * self.dim, kj * self.dim)
                bottom_right = ((ki + 1) * self.dim, (kj + 1) * self.dim)
                draw.rectangle(
                    [top_left, bottom_right],
                    outline=(10, 10, 10, 10),
                    fill=(10, 10, 10, 10),
                    width=self.dim / 2,
                )
        combined = Image.alpha_composite(im, overlay)
        combined.save(output_image_path)
        log.info(f'Wrote {output_image_path}')
        return output_image_path
