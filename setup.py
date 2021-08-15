"""Build & Install script for the pyrf24 package or python wrappers about
the RF24 C++ libraries."""
from skbuild import setup


long_description = ""
with open("README.rst", "r") as file_handle:
    long_description = file_handle.read()

# def exclude_rf24_utility_folder(cmake_manifest):
#     return list(filter(lambda name: not (name.endswith(".h")), cmake_manifest))

setup(
    name="pyrf24",
    # use_scm_version=True,
    author="2bndy5",
    author_email="2bndy5@gmail.com",
    description="A python package for the wrapping RF24 related C++ libraries",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/nRF24/pyRF24",
    packages=["pyrf24"],
    package_dir={"": "src"},
    cmake_install_dir="src/pyrf24",
    cmake_args=["-DRF24_DRIVER=SPIDEV"],
    # cmake_process_manifest_hook=exclude_rf24_utility_folder,
    zip_safe=False,
        license="GNU General Public License v2 (GPLv2)",
    classifiers=[
        "Development Status :: 1 - Planning",  # TODO change this when ready
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Topic :: System :: Hardware",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.7",
    keywords="nrf24l01 nRF24L01+ raspberry pi driver radio transceiver",
    # Extra links for the sidebar on pypi
    project_urls={
        "Documentation": "http://nRF24.github.io/pyRF24",
    },
    download_url="https://github.com/nRF24/pyRF24/releases",
)
