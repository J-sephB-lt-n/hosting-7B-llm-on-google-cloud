sudo apt-get update
# sudo apt-get install gcc git make -y
sudo apt-get install build-essential git -y
git clone https://github.com/ggerganov/llama.cpp

# if no GPU available #
cd llama.cpp && make && cd ..

# if cuda GPU available #
# refer to: https://cloud.google.com/compute/docs/gpus/install-drivers-gpu
cd llama.cpp && make make GGML_CUDA=1 && cd ..

mkdir llm_models
wget -O llm_models/model.gguf 'https://huggingface.co/internlm/internlm2_5-7b-chat-gguf/resolve/main/internlm2_5-7b-chat-q5_k_m.gguf?download=true'
sudo apt-get install python3-bs4 python3-requests -y
