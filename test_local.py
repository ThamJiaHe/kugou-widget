#!/usr/bin/env python3
"""
Local test script to verify the app works before deploying
"""
import sys
import os

# Change to api directory to simulate Vercel environment
api_dir = os.path.join(os.path.dirname(__file__), 'api')
os.chdir(api_dir)
sys.path.insert(0, api_dir)

print(f"Working directory: {os.getcwd()}")
print(f"sys.path: {sys.path[:3]}...")

print("\nTesting module imports from api directory...")
try:
    from kugou_client import KugouClient
    print("✅ kugou_client imported successfully")
except Exception as e:
    print(f"❌ Failed to import kugou_client: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

try:
    from svg_generator import generate_music_svg, generate_default_svg, generate_error_svg
    print("✅ svg_generator imported successfully")
except Exception as e:
    print(f"❌ Failed to import svg_generator: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\nTesting SVG generation...")
try:
    svg = generate_music_svg(
        song_name="Test Song - 测试",
        artist_name="Test Artist",
        album_cover_url="https://via.placeholder.com/300",
        theme="dark"
    )
    assert '<svg' in svg
    assert 'Test Song' in svg or '测试' in svg
    print("✅ SVG generation works")
    print(f"   SVG length: {len(svg)} bytes")
except Exception as e:
    print(f"❌ SVG generation failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\nTesting error SVG...")
try:
    error_svg = generate_error_svg("Test error", "light", 400, 120)
    assert '<svg' in error_svg
    print("✅ Error SVG generation works")
except Exception as e:
    print(f"❌ Error SVG failed: {e}")
    sys.exit(1)

print("\nTesting Flask app import...")
try:
    from index import app, DEMO_SONGS
    print("✅ Flask app imported successfully")
    print(f"   Demo songs: {len(DEMO_SONGS)}")
    print(f"   App routes: {[rule.rule for rule in app.url_map.iter_rules()]}")
except Exception as e:
    print(f"❌ Flask app import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n✅ All local tests passed!")
print("✅ Ready to deploy to Vercel")
