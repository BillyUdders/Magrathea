import os
import unittest
import sys

# Add the parent directory to sys.path to allow importing main
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import render_map_to_png

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

if __name__ == '__main__':
    unittest.main()
