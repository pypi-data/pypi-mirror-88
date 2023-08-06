![tensorfree](http://asmithcreations.com/tensorfree.png)

[![Build Status](https://travis-ci.com/andrew-alm/tensorfree.svg?branch=master)](https://travis-ci.com/andrew-alm/tensorfree)
[![Maintainability](https://api.codeclimate.com/v1/badges/119b0928e6f2a18b0c01/maintainability)](https://codeclimate.com/github/andrew-alm/tensorfree/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/119b0928e6f2a18b0c01/test_coverage)](https://codeclimate.com/github/andrew-alm/tensorfree/test_coverage)

Tensorfree is an image classification library that provides quick and easy access to some of the latest SOTA models. Simply install, define the location of your photos and let it do everything for you.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install tensorfree
```

## Usage

```python
from tensorfree import Tensorfree

# Here we create a new InceptionResNetV2 model
model = Tensorfree.build('InceptionResNetV2')
model.get_photos('photos/')
model.save_photos('labeled_photos/')
model.label()
```

#### Current Models Available

`NASNetLarge` : [Learning Transferable Architectures for Scalable Image Recognition](https://arxiv.org/abs/1707.07012)

`DenseNet` : [Densely Connected Convolutional Networks](https://arxiv.org/abs/1608.06993)

`MobileNetV2` : [MobileNetV2: Inverted Residuals and Linear Bottlenecks](https://arxiv.org/abs/1801.04381)

`InceptionResNetV2` : [Inception-v4, Inception-ResNet and the Impact of Residual Connections on Learning](https://arxiv.org/abs/1602.07261)

`VGG19` : [Very Deep Convolutional Networks for Large-Scale Image Recognition](https://arxiv.org/abs/1409.1556)

## Contributing
Contributions are welcome, and they are greatly appreciated! Every little bit helps, and credit will always be given. Please check [CONTRIBUTING.rst](https://github.com/andrew-alm/tensorfree/blob/master/CONTRIBUTING.rst) for more info.

## License
[MIT](https://choosealicense.com/licenses/mit/)


