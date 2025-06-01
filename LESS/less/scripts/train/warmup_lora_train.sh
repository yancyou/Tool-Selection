#!/usr/bin/env bash
# 一次性清理所有脚本的 CRLF 行尾
sed -i 's/\r$//' less/scripts/train/base_training_args.sh less/scripts/train/lora_train.sh "$0"

# 解析参数，默认使用真实数据目录
data_dir=${1:-"less/less_data"}
model_path=${2:-"meta-llama/Llama-2-7b-hf"}
percentage=${3:-"0.05"}  # percentage of the full data to train
data_seed=${4:-"3"}
job_name=${5:-"llama2-7b-p${percentage}-lora-seed${data_seed}"}

# 加载基础训练参数
source less/scripts/train/base_training_args.sh

# 设置输出目录
output_dir=../out/${job_name}
if [[ ! -d $output_dir ]]; then
    mkdir -p $output_dir
fi

# 定义训练文件列表
train_files=(
    "$data_dir/train/processed/flan_v2/flan_v2_data.jsonl"
    "$data_dir/train/processed/cot/cot_data.jsonl"
    "$data_dir/train/processed/dolly/dolly_data.jsonl"
    "$data_dir/train/processed/oasst1/oasst1_data.jsonl"
)

# 为大模型配置 FSDP
if [[ $model_path == "meta-llama/Llama-2-13b-hf" ]]; then
    base_training_args="$base_training_args --fsdp 'full_shard auto_wrap' --fsdp_config llama2_13b_finetune"
elif [[ $model_path == "mistralai/Mistral-7B-v0.1" ]]; then
    base_training_args="$base_training_args --fsdp 'full_shard auto_wrap' --fsdp_config mistral_7b_finetune"
fi

# 构建训练参数并执行
training_args="$base_training_args \
--model_name_or_path $model_path \
--output_dir $output_dir \
--percentage $percentage \
--data_seed $data_seed \
--train_files ${train_files[@]} 2>&1 | tee $output_dir/train.log"

eval "$header" "$training_args"