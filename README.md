Installation:

Step 1:
  git clone [the repository](https://github.com/Raizudeen-S/Lipsync_video/)
Step 2:
  Install the required version torch from pytorch wesite.
Step 3:
  Install Required Packages
  pip install -r requirements.txt
Step 4:
Resolve the error on the package 

Open ./stable-diffusion-webui/venv/lib/python3.10/site-packages/basicsr/data/degradations.py and on line 8, simply change:

from torchvision.transforms.functional_tensor import rgb_to_grayscale

to: from torchvision.transforms.functional import rgb_to_grayscale

Which should at least get you past this step.

Step 4:
 Run app.py package
 python app.py
