# hosting-7B-llm-on-google-cloud

In this repo, I'm seeing how fast the Large Language Model InternLM2.5-7B-Chat (q5_k_m quantized) runs on different Google Cloud Compute Engine Virtual Machines.

On each machine, I run the same 5 queries, which all involve answering questions based on ~1000 words of text taken from a website - you can see the benchmarking code here: [./query_speed_benchmark.py](./query_speed_benchmark.py)

| machine type  | GPU(s)      | specs                        | boot disk size | GCP Image                            | cost per hour | mean inference time (single query) | all inference times (single queries)         |
| ------------- | ----------- | ---------------------------- | -------------- | ------------------------------------ | ------------- | ---------------------------------- | -------------------------------------------- |
| e2-himem-2    | 0           | 2 vCPU, 1 core, 16GB memory  | 10 Gb          |                                      | $0.12         | 15 minutes                         | 878 (I got bored and stopped after this one) |
| e2-himem-4    | 0           | 4 vCPU, 2 core, 32Gb memory  | 10 Gb          |                                      | $0.23         | 7 minutes                          | 418, 440, 422, 419, 435                      |
| e2-himem-8    | 0           | 8 vCPU, 4 core, 64 GB memory | 10 Gb          |                                      | $0.47         | 3.5 minutes                        | 205, 215, 209, 204, 215                      |
| n1-standard-4 | 1 Nvidia T4 | 4 vCPU, 2 core, 15 GB memory | 50 Gb          | Deep Learning VM with CUDA 11.8 M123 | $0.67         | 20 seconds                         | 7, 30, 13, 12, 41                            |

Code used for VM setup:

[./setup_vm.sh](./setup_vm.sh)

Run the benchmark on a virtual machine:

```bash
# launch a local model server #
llama.cpp/llama-server -m './llm_models/model.gguf' --port 6969 --ctx-size 2000 > /dev/null 2>&1 &
# run the benchmark #
python3 query_speed_benchmark.py
# stop the local model server #
pkill llama-server
```
