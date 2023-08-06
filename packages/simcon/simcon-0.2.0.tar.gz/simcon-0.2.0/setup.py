import os
import os.path

from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension, build_ext


MSFS_SDK = os.environ.get("MSFS_SDK")
if not MSFS_SDK:
    raise EnvironmentError("MSFS_SDK environment variable is not defined. Do you have MSFS SDK installed?")
MSFS_INCLUDE_DIR = os.path.join(MSFS_SDK, "SimConnect SDK\\include")
MSFS_LIB_DIR = os.path.join(MSFS_SDK, "SimConnect SDK\\lib\\static")

simcon_root = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(simcon_root, "README.md")) as readme_fh:
    readme = readme_fh.read()

setup(
    name="simcon",
    version="0.2.0",
    author="Roman Andriadi",
    author_email="simcon@narn.me",
    description="MSFS SimConnect wrapper for Python",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/nARNcheg/py-simcon",
    classifiers=[
        "Operating System :: Microsoft :: Windows",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Programming Language :: Python :: 3",
        "Topic :: Games/Entertainment",
        "Typing :: Typed",
    ],
    python_requires=">=3.7",
    packages=["simcon"],
    ext_modules=[
        Pybind11Extension(
            "simcon._native",
            ["native/pybind.cpp", "native/sim.cpp"],
            include_dirs=[MSFS_INCLUDE_DIR],
            library_dirs=[MSFS_LIB_DIR],
            extra_link_args=["/DEBUG:FULL"],
            libraries=[  # Documentation/04-Developer_Tools/SimConnect/SimConnect_Reference.html#programming-simconnect-clients-using-managed-code
                "SimConnect",
                "shlwapi",
                "user32",
                "Ws2_32",
                "Advapi32",
                "Shell32",
            ],
        ),
    ],
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
    package_data={
        "simcon": ["*.pyi", "py.typed"],
    },
)
