import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='keras_conv_visualizer',
    version='0.0.1',
    author="Albert Lis",
    author_email="albert.lis.1996@gmail.com",
    description="Package allows visualize convolutional layers from keras models.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/albertlis/keras-conv-visualizer",
    packages=setuptools.find_packages(),
    install_requires=[
        "tensorflow >= 2.0",
        "numpy >= 1.0",
        "opencv-python >= 4.0",
        "matplotlib >= 3.0"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
