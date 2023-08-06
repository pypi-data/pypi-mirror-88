from setuptools import setup
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='VisionRPA',
    version='0.1.2',    
    description='VisionUI is a RPA product, which can be used for differen automation processes',
    author='ExpertVision',
    author_email='ayazpk6630@gmail.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['VisionRPA'],
    install_requires=['MouseInfo==0.1.3',
                        'numpy==1.19.4',
                        'opencv-python==4.4.0.46',
                        'pandas==1.1.5',
                        'Pillow==8.0.1',
                        'PyAutoGUI==0.9.52',
                        'PyGetWindow==0.0.9',
                        'PyMsgBox==1.0.9',
                        'pyperclip==1.8.1',
                        'PyRect==0.1.4',
                        'PyScreeze==0.1.26',
                        'python-dateutil==2.8.1',
                        'PyTweening==1.0.3',
                        'pytz==2020.4',
                        'pywin32==300',
                        'six==1.15.0',
                   
                      ],

    classifiers=[
        'Intended Audience :: Science/Research', 
        'Operating System :: Microsoft :: Windows',        
        'Programming Language :: Python :: 3.5',
    ],
)