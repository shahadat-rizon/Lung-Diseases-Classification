from setuptools import setup, find_packages

setup(
    name="lung-diseases-classification",
    version="1.0.0",
    description="Lung Diseases Classification using Machine Learning and Deep Learning",
    author="Shahadat Rizon",
    author_email="",
    packages=find_packages(),
    install_requires=[
        "tensorflow>=2.10.0",
        "scikit-learn>=1.2.0",
        "xgboost>=1.7.0",
        "numpy>=1.21.0",
        "matplotlib>=3.5.0",
        "seaborn>=0.11.0",
        "Pillow>=9.0.0",
        "jupyter>=1.0.0",
        "ipykernel>=6.0.0",
        "pandas>=1.4.0",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)