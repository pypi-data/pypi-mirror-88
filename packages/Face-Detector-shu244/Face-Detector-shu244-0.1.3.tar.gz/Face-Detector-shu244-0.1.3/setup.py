from setuptools import setup, find_packages


REQUIRED_PACKAGES = ['opencv-python==4.4.0.46',
                     'torch==1.6.0',
                     'numpy==1.19.1',
                     'torchvision==0.7.0',
                     'matplotlib==3.3.1',
                     'Pillow==8.0.1']

setup(
    name='Face-Detector-shu244',
    version='0.1.3',
    author="Shuhao Lai",
    author_email="Shuhaolai18@gmail.com",
    description="Extract faces from images",
    packages=find_packages(include=['face_detector', 'face_detector.*']),
    install_requires=REQUIRED_PACKAGES
)