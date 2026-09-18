"""Create a vector-preserving, two-up portrait A4 invoice print PDF."""
import argparse
import math
from pathlib import Path

from pypdf import PdfReader, PdfWriter, Transformation
from pypdf.generic import RectangleObject


def combine(inputs, output):
    sources = [Path(value).resolve(strict=True) for value in inputs]
    target = Path(output).resolve()
    if target in sources:
        raise ValueError('Output must not replace a source PDF.')
    if target.exists():
        raise FileExistsError(f'Choose a new output filename: {target}')
    readers = [PdfReader(path) for path in sources]
    for reader in readers:
        if reader.is_encrypted and not reader.decrypt(''):
            raise ValueError('Password-protected input requires an unlocked copy.')
    total = sum(len(reader.pages) for reader in readers)
    if not total:
        raise ValueError('No source pages found.')
    width, height = 210 / 25.4 * 72, 297 / 25.4 * 72
    margin = 20
    writer = PdfWriter()
    index = 0
    for reader in readers:
        for source in reader.pages:
            if source.rotation:
                source.transfer_rotation_to_content()
            box = source.cropbox
            left, bottom = float(box.left), float(box.bottom)
            sw, sh = float(box.width), float(box.height)
            if sw <= 0 or sh <= 0:
                raise ValueError('Source has an invalid visible page size.')
            # Normalize nonzero crop-box origins and clip to the visible region.
            source.add_transformation(Transformation().translate(-left, -bottom))
            source.mediabox = RectangleObject((0, 0, sw, sh))
            source.cropbox = RectangleObject((0, 0, sw, sh))
            if index % 2 == 0:
                page = writer.add_blank_page(width, height)
            scale = min((width - 2 * margin) / sw,
                        (height / 2 - 2 * margin) / sh)
            x = (width - sw * scale) / 2
            y = (height / 2 if index % 2 == 0 else 0)
            y += (height / 2 - sh * scale) / 2
            page.merge_transformed_page(
                source, Transformation().scale(scale).translate(x, y))
            index += 1
    target.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive creation also protects existing outputs against accidental overwrite.
    with target.open('xb') as stream:
        writer.write(stream)
    result = PdfReader(target)
    assert len(result.pages) == math.ceil(total / 2)
    for page in result.pages:
        assert abs(float(page.mediabox.width) - width) < 0.01
        assert abs(float(page.mediabox.height) - height) < 0.01
    print(f'{total} source pages -> {len(result.pages)} A4 pages: {target}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True)
    parser.add_argument('inputs', nargs='+')
    args = parser.parse_args()
    combine(args.inputs, args.output)

