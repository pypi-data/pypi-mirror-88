import setuptools
setuptools.setup(
  name="ty.print",
  version="1.0",
  author="石卓然",
  author_email="2720791562@qq.com",
  description="让你能使用o_print代码实现逐字输出！",
  long_description="一个能让你使用“o_print”代码快速实现逐字输出的效果的库。",
  long_description_content_type="text/markdown",
  url="https://zanwu.meiyou",
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)
REQUIRED = [
    "sys","time",
]
