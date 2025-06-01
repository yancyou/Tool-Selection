#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
脚本功能：按顺序重写JSONL文件中的 'id' 字段为连续的整数（从0开始）。
用法：
    python replace_ids_sequential.py input.json output.jsonl
"""

import json
import sys
import argparse
from json import JSONDecoder

def main():
    parser = argparse.ArgumentParser(description='按顺序重写JSONL文件中的id字段')
    parser.add_argument('input_file', nargs='?', default='data/ToolBench/toolllama_G123_dfs_eval.json', help='输入文件路径（JSONL格式）')
    parser.add_argument('output_file', nargs='?', default='data/ToolBench/toolllama_G123_dfs_eval_LESS.jsonl', help='输出文件路径（JSONL格式）')
    parser.add_argument('--encoding', default='utf-8', help='文件编码，默认为utf-8')
    args = parser.parse_args()

    # 读取输入文件
    try:
        with open(args.input_file, 'r', encoding=args.encoding) as inf:
            content = inf.read().strip()
        
        # 尝试解析为JSON数组
        try:
            # 首先尝试作为单个JSON数组解析
            records = json.loads(content)
            if not isinstance(records, list):
                records = [records]
        except json.JSONDecodeError:
            # 如果不是单个JSON，尝试按行解析JSONL
            records = []
            for line in content.split('\n'):
                if line.strip():
                    try:
                        records.append(json.loads(line))
                    except json.JSONDecodeError as e:
                        print(f"警告: 跳过无法解析的行: {e}", file=sys.stderr)
    except Exception as e:
        print(f"错误: 无法读取或解析输入文件: {e}", file=sys.stderr)
        sys.exit(1)

    # 写入输出，确保每个对象单独一行
    with open(args.output_file, 'w', encoding=args.encoding) as outf:
        for idx, obj in enumerate(records):
            # 更新ID
            obj['id'] = idx
            # 将完整对象写为单行JSON
            outf.write(json.dumps(obj, ensure_ascii=False) + '\n')
    
    print(f"处理完成: {len(records)}条记录已写入{args.output_file}")

if __name__ == '__main__':
    main() 