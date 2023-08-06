from setuptools import setup, find_packages


REQUIRED_PACKAGES = ['opencv-python==4.4.0.46',
                     'torch==1.6.0',
                     'numpy==1.19.1',
                     'torchvision==0.7.0',
                     'matplotlib',
                     'Pillow==8.0.1']

setup(
    name='Face-Detector-shu244',
    version='0.1.0',
    author="Shuhao Lai",
    author_email="Shuhaolai18@gmail.com",
    description="Extract faces from images",
    packages=find_packages(include=['face_detector',
                                    'face_detector.utils.*',
                                    'face_detector.interface.py',
                                    'face_detector.models.py']),
    install_requires=REQUIRED_PACKAGES
)