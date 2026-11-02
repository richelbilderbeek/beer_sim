#!/usr/bin/env python3
"""Play the WebAssembly game on the 'Play' page of a built website.

Usage: test_play_page.py <URL of the play page>

Compares what the browser shows to the images of the game:
the game must show up without a title bar, the foam must disappear
over time and clicking must bring it back.
"""
import io
import sys
import time

from PIL import Image, ImageChops, ImageStat
from playwright.sync_api import sync_playwright

GIRL_POS = (9, 9)
BEER_LABEL = (578, 241, 61, 121)  # x, y, width, height, see game_dialog.ui
START_TIMEOUT_SECS = 60
# The foam disappears with a chance of 1 in 10 per second
FOAM_TIMEOUT_SECS = 120
MAX_DIFF = 12  # Average difference per color channel, from 0 to 255


def diff(image_a, image_b):
    """Average difference per color channel between two images."""
    stat = ImageStat.Stat(ImageChops.difference(image_a, image_b))
    return sum(stat.mean) / len(stat.mean)


def expected_beer(background, filename):
    """What the part of the game with the beer should look like."""
    beer = Image.open(filename).convert("RGBA")
    x, y, width, height = BEER_LABEL
    box = (x, y, x + width, y + height)
    result = background.crop(box).convert("RGBA")
    # A QLabel centers its pixmap vertically
    result.alpha_composite(beer, (0, (height - beer.height) // 2))
    return result.convert("RGB"), box


def main():
    url = sys.argv[1]
    girl = Image.open("girl.png").convert("RGBA")
    background = Image.new("RGBA", (824, 818), (0, 0, 0, 255))
    background.alpha_composite(girl, GIRL_POS)
    with_foam, box = expected_beer(background, "beer_with_foam.png")
    no_foam, _ = expected_beer(background, "beer_no_foam.png")
    # The part of the girl that is never covered by anything
    girl_box = (9, 400, 400, 800)
    expected_girl = background.crop(girl_box).convert("RGB")

    errors = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 1300})
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.on("console", lambda m: print(f"console: {m.text}"))
        page.goto(url)
        frame = page.locator("iframe")

        def screenshot():
            data = frame.screenshot()
            return Image.open(io.BytesIO(data)).convert("RGB")

        def beer_state():
            shot = screenshot()
            crop = shot.crop(box)
            return diff(crop, with_foam), diff(crop, no_foam)

        print("Waiting for the game to show up")
        deadline = time.time() + START_TIMEOUT_SECS
        girl_diff = 255.0
        while time.time() < deadline and girl_diff > MAX_DIFF:
            shot = screenshot()
            girl_diff = diff(shot.crop(girl_box), expected_girl)
            print(f"Difference with the expected girl: {girl_diff:.1f}")
            time.sleep(1)
        assert girl_diff <= MAX_DIFF, "Game not shown at the expected spot"
        assert not errors, errors

        print("Waiting for the foam to disappear")
        deadline = time.time() + FOAM_TIMEOUT_SECS
        foam_diff, no_foam_diff = beer_state()
        assert foam_diff <= MAX_DIFF, f"No foam at start: {foam_diff:.1f}"
        while time.time() < deadline and no_foam_diff > MAX_DIFF:
            time.sleep(1)
            foam_diff, no_foam_diff = beer_state()
        assert no_foam_diff <= MAX_DIFF, f"Foam stayed: {no_foam_diff:.1f}"

        print("Clicking to get foam again")
        frame.click(position={"x": 100, "y": 100})
        time.sleep(1)
        foam_diff, _ = beer_state()
        assert foam_diff <= MAX_DIFF, f"Click gave no foam: {foam_diff:.1f}"
        assert not errors, errors
        browser.close()
    print("OK: the game can be played")


if __name__ == "__main__":
    main()
