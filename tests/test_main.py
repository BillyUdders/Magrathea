import os
import unittest

from magrathea.main import render_map_to_png, render_map_to_buffer

class TestMapRendering(unittest.TestCase):
    def test_render_png(self):
        filename = "test_output.png"
        # Ensure file doesn't exist before test
        if os.path.exists(filename):
            os.remove(filename)
            
        render_map_to_png(64, 2, filename)
        
        self.assertTrue(os.path.exists(filename), "PNG file should be created")
        
        # Cleanup
        if os.path.exists(filename):
            os.remove(filename)

    def test_render_buffer(self):
        buf = render_map_to_buffer(64, 2)
        self.assertTrue(buf.getbuffer().nbytes > 0, "Buffer should contain data")
        buf.close()

if __name__ == '__main__':
    unittest.main()
