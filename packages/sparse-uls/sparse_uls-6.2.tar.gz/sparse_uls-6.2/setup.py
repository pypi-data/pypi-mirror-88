import setuptools

with open("./README.md", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="sparse_uls",
    version="6.2",
    author="Nguyen Ngoc Khanh",
    author_email="nguyenngockhanh.pbc@gmail.com",
    description="optimize norm with underdetermined system equality constraint",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/khanhhhh/sparse-uls",
    packages=setuptools.find_packages(),
)
