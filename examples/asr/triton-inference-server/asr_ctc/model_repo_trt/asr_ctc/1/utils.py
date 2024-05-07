import torch
import tensorrt as trt
import os

TRT_LOGGER = trt.Logger()

class TrtInfer():
    def __init__(self, engine_file, device='cuda'):
        self.engine_file = engine_file
        self.engine = self.load_engine(engine_file)
        self.context = self.engine.create_execution_context()
        self.device = device
    
    def load_engine(self, engine_file_path):
        assert os.path.exists(engine_file_path)
        print("Reading engine from file {}".format(engine_file_path))
        with open(engine_file_path, "rb") as f, trt.Runtime(TRT_LOGGER) as runtime:
            return runtime.deserialize_cuda_engine(f.read())
    
    def infer_encoder(self, batch_tensor, do_test=False):
        stream = torch.cuda.Stream()
        # torch.cuda.current_stream
        return self.trt_infer(self.context, batch_tensor, stream)
     
    def trt_infer(self, context, batch_pyt_tensor, stream):
        audio_signal, length = batch_pyt_tensor
        audio_signal = audio_signal.contiguous()
        length = length.contiguous()
        audio_signal = audio_signal.to(device=self.device)
        length = length.to(device=self.device)
        context.set_input_shape("audio_signal", audio_signal.shape) 
        context.set_tensor_address('audio_signal', audio_signal.data_ptr())
        context.set_input_shape("length", length.shape)  # b,
        context.set_tensor_address('length', length.data_ptr())
        log_probs = torch.zeros(tuple(context.get_tensor_shape("log_probs")), \
                                dtype=torch.float32, device=self.device).contiguous()
        encoded_length = torch.zeros(tuple(context.get_tensor_shape("encoded_length")), \
                                     dtype=torch.int32, device=self.device).contiguous()
        context.set_tensor_address('log_probs', log_probs.data_ptr())
        context.set_tensor_address('encoded_length', encoded_length.data_ptr())

        context.execute_async_v3(stream_handle=stream.cuda_stream)
        stream.synchronize()
        return log_probs, encoded_length