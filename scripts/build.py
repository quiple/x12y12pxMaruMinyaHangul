import logging
import math
import shutil
from pathlib import Path

from kbitfont import KbitFont, KbitGlyph, KbitProps
from pixel_font_builder import FontBuilder, WeightName, SerifStyle, SlantStyle, WidthStyle, Glyph, opentype


def _create_glyph(name: str, kbit_glyph: KbitGlyph, kbit_props: KbitProps) -> Glyph:
    return Glyph(
        name=name,
        horizontal_offset=(kbit_glyph.x, kbit_glyph.y - kbit_glyph.height),
        advance_width=kbit_glyph.advance,
        vertical_offset=(kbit_glyph.width // 2, kbit_props.em_ascent - kbit_glyph.y),
        advance_height=kbit_props.em_height,
        bitmap=[[0 if color <= 127 else 1 for color in bitmap_row] for bitmap_row in kbit_glyph.bitmap],
    )


def main():
    logging.basicConfig(level=logging.DEBUG)

    project_root_dir = Path(__file__).parent.joinpath('..').resolve()

    outputs_dir = project_root_dir.joinpath('outputs')
    if outputs_dir.exists():
        shutil.rmtree(outputs_dir)
    outputs_dir.mkdir(parents=True, exist_ok=True)

    kbit_font = KbitFont.load_kbitx(project_root_dir.joinpath('src', 'x12y12pxMaruMinyaHangul.kbitx'))

    builder = FontBuilder()
    builder.font_metric.font_size = kbit_font.props.em_height
    builder.font_metric.horizontal_layout.ascent = kbit_font.props.line_ascent
    builder.font_metric.horizontal_layout.descent = -kbit_font.props.line_descent
    builder.font_metric.horizontal_layout.line_gap = kbit_font.props.line_gap
    builder.font_metric.vertical_layout.ascent = math.ceil(kbit_font.props.line_height / 2)
    builder.font_metric.vertical_layout.descent = -math.floor(kbit_font.props.line_height / 2)
    builder.font_metric.vertical_layout.line_gap = kbit_font.props.line_gap
    builder.font_metric.x_height = kbit_font.props.x_height
    builder.font_metric.cap_height = kbit_font.props.cap_height

    builder.meta_info.version = '0.0.0'
    builder.meta_info.family_name = kbit_font.names.family
    builder.meta_info.weight_name = WeightName.REGULAR
    builder.meta_info.serif_style = SerifStyle.SANS_SERIF
    builder.meta_info.slant_style = SlantStyle.NORMAL
    builder.meta_info.width_style = WidthStyle.MONOSPACED
    builder.meta_info.manufacturer = kbit_font.names.manufacturer
    builder.meta_info.designer = kbit_font.names.designer
    builder.meta_info.description = kbit_font.names.description
    builder.meta_info.copyright_info = kbit_font.names.copyright
    builder.meta_info.license_info = kbit_font.names.license_description
    builder.meta_info.vendor_url = kbit_font.names.vendor_url
    builder.meta_info.designer_url = kbit_font.names.designer_url
    builder.meta_info.license_url = kbit_font.names.license_url

    builder.glyphs.append(_create_glyph('.notdef', kbit_font.named_glyphs['.notdef'], kbit_font.props))

    for code_point, kbit_glyph in sorted(kbit_font.characters.items()):
        glyph_name = f'U+{code_point:04X}'
        builder.character_mapping[code_point] = glyph_name
        builder.glyphs.append(_create_glyph(glyph_name, kbit_glyph, kbit_font.props))

    builder.save_otf(outputs_dir.joinpath('x12y12pxMaruMinyaHangul.otf'))
    print('x12y12pxMaruMinyaHangul.otf')
    builder.save_otf(outputs_dir.joinpath('x12y12pxMaruMinyaHangul.otf.woff'), flavor=opentype.Flavor.WOFF)
    print('x12y12pxMaruMinyaHangul.otf.woff')
    builder.save_otf(outputs_dir.joinpath('x12y12pxMaruMinyaHangul.otf.woff2'), flavor=opentype.Flavor.WOFF2)
    print('x12y12pxMaruMinyaHangul.otf.woff2')
    builder.save_ttf(outputs_dir.joinpath('x12y12pxMaruMinyaHangul.ttf'))
    print('x12y12pxMaruMinyaHangul.ttf')
    builder.save_ttf(outputs_dir.joinpath('x12y12pxMaruMinyaHangul.ttf.woff'), flavor=opentype.Flavor.WOFF)
    print('x12y12pxMaruMinyaHangul.ttf.woff')
    builder.save_ttf(outputs_dir.joinpath('x12y12pxMaruMinyaHangul.ttf.woff2'), flavor=opentype.Flavor.WOFF2)
    print('x12y12pxMaruMinyaHangul.ttf.woff2')
    builder.save_ms_bitmap_ttf(outputs_dir.joinpath('x12y12pxMaruMinyaHangul.ms.bitmap.ttf'))
    print('x12y12pxMaruMinyaHangul.ms.bitmap.ttf')
    builder.save_otb(outputs_dir.joinpath('x12y12pxMaruMinyaHangul.otb'))
    print('x12y12pxMaruMinyaHangul.otb')
    builder.save_dfont(outputs_dir.joinpath('x12y12pxMaruMinyaHangul.dfont'))
    print('x12y12pxMaruMinyaHangul.dfont')
    builder.save_bdf(outputs_dir.joinpath('x12y12pxMaruMinyaHangul.bdf'))
    print('x12y12pxMaruMinyaHangul.bdf')
    builder.save_pcf(outputs_dir.joinpath('x12y12pxMaruMinyaHangul.pcf'))
    print('x12y12pxMaruMinyaHangul.pcf')

    builder.meta_info.family_name = f'{kbit_font.names.family} SquareDot'
    builder.opentype_config.outlines_painter = opentype.SquareDotOutlinesPainter()
    builder.save_otf(outputs_dir.joinpath('x12y12pxMaruMinyaHangul-SquareDot.otf'))
    print('x12y12pxMaruMinyaHangul-SquareDot.otf')
    builder.save_otf(outputs_dir.joinpath('x12y12pxMaruMinyaHangul-SquareDot.otf.woff'), flavor=opentype.Flavor.WOFF)
    print('x12y12pxMaruMinyaHangul-SquareDot.otf.woff')
    builder.save_otf(outputs_dir.joinpath('x12y12pxMaruMinyaHangul-SquareDot.otf.woff2'), flavor=opentype.Flavor.WOFF2)
    print('x12y12pxMaruMinyaHangul-SquareDot.otf.woff2')
    builder.save_ttf(outputs_dir.joinpath('x12y12pxMaruMinyaHangul-SquareDot.ttf'))
    print('x12y12pxMaruMinyaHangul-SquareDot.ttf')
    builder.save_ttf(outputs_dir.joinpath('x12y12pxMaruMinyaHangul-SquareDot.ttf.woff'), flavor=opentype.Flavor.WOFF)
    print('x12y12pxMaruMinyaHangul-SquareDot.ttf.woff')
    builder.save_ttf(outputs_dir.joinpath('x12y12pxMaruMinyaHangul-SquareDot.ttf.woff2'), flavor=opentype.Flavor.WOFF2)
    print('x12y12pxMaruMinyaHangul-SquareDot.ttf.woff2')

    builder.meta_info.family_name = f'{kbit_font.names.family} CircleDot'
    builder.opentype_config.outlines_painter = opentype.CircleDotOutlinesPainter()
    builder.save_otf(outputs_dir.joinpath('x12y12pxMaruMinyaHangul-CircleDot.otf'))
    print('x12y12pxMaruMinyaHangul-CircleDot.otf')
    builder.save_otf(outputs_dir.joinpath('x12y12pxMaruMinyaHangul-CircleDot.otf.woff'), flavor=opentype.Flavor.WOFF)
    print('x12y12pxMaruMinyaHangul-CircleDot.otf.woff')
    builder.save_otf(outputs_dir.joinpath('x12y12pxMaruMinyaHangul-CircleDot.otf.woff2'), flavor=opentype.Flavor.WOFF2)
    print('x12y12pxMaruMinyaHangul-CircleDot.otf.woff2')
    builder.save_ttf(outputs_dir.joinpath('x12y12pxMaruMinyaHangul-CircleDot.ttf'))
    print('x12y12pxMaruMinyaHangul-CircleDot.ttf')
    builder.save_ttf(outputs_dir.joinpath('x12y12pxMaruMinyaHangul-CircleDot.ttf.woff'), flavor=opentype.Flavor.WOFF)
    print('x12y12pxMaruMinyaHangul-CircleDot.ttf.woff')
    builder.save_ttf(outputs_dir.joinpath('x12y12pxMaruMinyaHangul-CircleDot.ttf.woff2'), flavor=opentype.Flavor.WOFF2)
    print('x12y12pxMaruMinyaHangul-CircleDot.ttf.woff2')


if __name__ == '__main__':
    main()
