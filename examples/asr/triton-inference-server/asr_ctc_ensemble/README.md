convert nemo ctc model to onnx:
```
mkdir onnx_model/
python3 NeMo/examples/asr/triton-inference-server/scripts/export_asr_ctc_onnx.py --nemo_model=parakeet-ctc-1.1b/parakeet-ctc-1.1b.nemo --onnx_model=onnx_model/model.onnx

# OR

python3 NeMo/examples/asr/triton-inference-server/scripts/export_asr_ctc_onnx.py --pretrained_model=nvidia/parakeet-ctc-1.1b --onnx_model=onnx_model/model.onnx

```

*Don't use `NeMo/scripts/export.py` to export the model to onnx.*

Convert onnx model to tensorrt:
```
docker run --gpus all -it -v $PWD:/ws nvcr.io/nvidia/tensorrt:24.02-py3
trtexec --onnx=onnx_model/model.onnx \
        --minShapes=audio_signal:1x80x100,length:1 \
        --optShapes=audio_signal:16x80x1024,length:16 \
        --maxShapes=audio_signal:32x80x3500,length:32 \
        --fp16 \
        --saveEngine=encoder.trt
                                     
```
The input is from 1 seconds to 60 seconds (1min).

|GPU      | Throughput/QPS | inputShape| TRT|
|V100     | 9.57           | 16x80x1000| 863|
|A100-PCIE| 19.28          | 16x80x1024| 863|
|A100-PCIE| 24.99          | 16x80x1024| 100|  


```
mv encoder.trt encoder/1/
```

## Performance
TRT863 & A100 PCIE
|concurrency | dtype | num instance| RTFx|duration|sorted|allow_ragged_batch|
|------------|-------|-------------|-----|--------|------|------------------|
|10          | fp16  | 2           |     | 96     | T    | T                |
