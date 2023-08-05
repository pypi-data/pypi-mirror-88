import setuptools.command.build_py
from setuptools import find_packages, setup

# Set version_info[__version__], while avoiding importing numpy, in case numpy
# and vg are being installed concurrently.
# https://packaging.python.org/guides/single-sourcing-package-version/
version_info = {}
exec(open("proximity/package_version.py").read(), version_info)

with open("README.md") as f:
    readme = f.read()

with open("requirements.txt") as f:
    install_requires = f.read()

exclude = ["**/test_*.py"]


class build_py(setuptools.command.build_py.build_py):
    def find_package_modules(self, package, package_dir):
        import fnmatch

        return [
            (pkg, mod, file)
            for (pkg, mod, file) in super().find_package_modules(package, package_dir)
            if not any(fnmatch.fnmatchcase(file, pat=pattern) for pattern in exclude)
        ]


setup(
    name="proximity",
    version=version_info["__version__"],
    description="Simple scenegraph for quickly debugging 3D meshes, polylines, and points",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Michael Dawson-Haggerty, Metabolize, Minnow Software, and other contributors",
    author_email="github@paulmelnikow.com",
    url="https://github.com/lace/proximity",
    project_urls={
        "Issue Tracker": "https://github.com/lace/proximity/issues",
        "Documentation": "https://proximity.readthedocs.io/en/stable/",
    },
    packages=find_packages(),
    install_requires=install_requires,
    cmdclass={"build_py": build_py},
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Manufacturing",
        "Topic :: Artistic Software",
        "Topic :: Multimedia :: Graphics :: 3D Modeling",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
)
