import setuptools


try:
    version = open('VERSION').read()
except FileNotFoundError:
    version = "local"

setuptools.setup(
    name='mkdocs-nav-includer-plugin',
    version=version,
    description='Plugin for improving nav in Mkdocs.',
    long_description="""""",  # noqa: E501
    keywords='mkdocs nav includer',
    url='https://github.com/TEDmn/mkdocs-nav-includer-plugin',
    author='Teddy "TEDmk" Turquet',
    author_email='teddy.turquet@protonmail.com',
    license='MIT',
    python_requires='>=3',
    install_requires=[
        'mkdocs>=1.0.4',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    packages=["mkdocs_nav_includer_plugin"],
    entry_points={
        'mkdocs.plugins': [
            "navincluder = mkdocs_nav_includer_plugin.plugin:NavIncluderPlugin"
        ]
    }
)
