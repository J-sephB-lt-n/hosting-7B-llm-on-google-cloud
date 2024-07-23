# hosting-7B-llm-on-google-cloud

| machine type                       | specs                       | cost per hour | mean inference time | all inference times     |
| ---------------------------------- | --------------------------- | ------------- | ------------------- | ----------------------- |
| e2-himem-2                         | 2 vCPU, 1 core, 16GB memory | $0.12         |                     |                         |
| e2-himem-4                         |                             |               |                     | 418, 440, 422, 419, 435 |
| e2-himem-8                         |                             |               |                     | 205, 215, 209, 204, 215 |
| n1-standard-4 with 1 nvidia T4 gpu |                             | $0.46         |                     |                         |

Code used for VM setup:

[./setup_vm.sh](./setup_vm.sh)

Run the benchmark on a machine:

```bash
# launch a local model server #
llama.cpp/llama-server -m './llm_models/model.gguf' --port 8080 --ctx-size 2000 > /dev/null 2>&1 &
# run the benchmark #
python3 query_speed_benchmark.py
# stop the local model server #
pkill llama-server
```
