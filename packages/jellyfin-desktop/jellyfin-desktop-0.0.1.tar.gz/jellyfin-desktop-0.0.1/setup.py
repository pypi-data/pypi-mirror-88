from setuptools import setup

setup(
    name="jellyfin-desktop",
    version="0.0.1",
    author="Ian Walton",
    author_email="iwalton3@gmail.com",
    description="Alias for jellyfin-mpv-shim to avoid squatting.",
    license="GPLv3",
    url="https://github.com/iwalton3/jellyfin-mpv-shim",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "jellyfin-mpv-shim"
    ]
)
