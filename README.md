# Tool Selection

This repository contains various dataset pruning methods for tool datasets. It serves as a collection of approaches for selecting high-quality data samples to improve model performance on tool-related tasks.

## Methods Included

### 1. LESS (Selecting Influential Data for Targeted Instruction Tuning)

LESS is a data selection method proposed in the ICML 2024 paper [LESS: Selecting Influential Data for Targeted Instruction Tuning](https://arxiv.org/abs/2402.04333). It focuses on selecting influential data to induce a target capability.

[Explore the LESS method](./LESS/README.md)

### 2. More Methods Coming Soon

We plan to add more dataset selection methods to this repository. Stay tuned for updates!

## Overview

Data selection is crucial for efficiently training models for specific tasks. This repository aims to provide researchers and practitioners with a collection of effective methods for dataset pruning, particularly focused on tool datasets.

Each method is contained in its own directory with detailed documentation and implementation code.

## Contributing

We welcome contributions! If you have a new method for dataset pruning or improvements to existing methods, please consider submitting a pull request.

## License

Please check the license information in each method's directory.

# LESS - Less is More for Data Selection

本仓库是[LESS](https://github.com/princeton-nlp/LESS)项目的定制版本，修改了部分训练脚本以支持自定义数据集。

## 主要修改

- 修改了`warmup_lora_train.sh`脚本以支持自定义数据格式
- 调整了训练参数，优化了模型性能

## 如何使用

### 准备数据

确保您的数据按照以下格式组织：
```
data/
  apibench/
    torchhub_train.json
    tensorflow_train.json
    huggingface_train.json
```

### Warmup训练

使用以下命令开始warmup训练：

```bash
DATA_DIR=./data  # 指向您的数据目录
MODEL_PATH=meta-llama/Llama-2-7b-hf  # 预训练模型路径
PERCENTAGE=0.05  # 使用数据的百分比
DATA_SEED=3  # 随机种子
JOB_NAME=llama2-7b-p${PERCENTAGE}-lora-seed${DATA_SEED}

./LESS/less/scripts/train/warmup_lora_train.sh "$DATA_DIR" "$MODEL_PATH" "$PERCENTAGE" "$DATA_SEED" "$JOB_NAME"
```

### 自定义训练参数

您可以通过修改`LESS/less/scripts/train/base_training_args.sh`文件来调整训练参数，如：

- 学习率
- 批次大小
- 训练轮数
- LoRA参数

## 注意事项

- 对于大于100MB的数据文件，请使用Git LFS进行管理
- 训练结果将保存在`../out/${JOB_NAME}`目录 