import sys
import torchvision.transforms.functional as F
 
# Create a dummy module to patch the missing import
import types
patched_module = types.ModuleType("functional_tensor")
patched_module.rgb_to_grayscale = F.rgb_to_grayscale
 
# Replace the missing import in sys.modules
sys.modules['torchvision.transforms.functional_tensor'] = patched_module