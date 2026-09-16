---
license: cc-by-nc-4.0
task_categories:
- text-classification
language:
- zh
tags:
- legal
pretty_name: ChineseSafe
size_categories:
- 10K<n<100K
---
## ChineseSafe
Dataset for [ChineseSafe: A Chinese Benchmark for Evaluating Safety in Large Language Models](https://arxiv.org/abs/2410.18491)

## Usage
```python
from datasets import load_dataset
dataset = load_dataset("SUSTech/ChineseSafe", split="test")
```

## Citation

If you find our dataset useful, please cite:
```
@article{zhang2024chinesesafe,
  title={ChineseSafe: A Chinese Benchmark for Evaluating Safety in Large Language Models},
  author={Zhang, Hengxiang and Gao, Hongfu and Hu, Qiang and Chen, Guanhua and Yang, Lili and Jing, Bingyi and Wei, Hongxin and Wang, Bing and Bai, Haifeng and Yang, Lei},
  journal={arXiv preprint arXiv:2410.18491},
  year={2024}
}