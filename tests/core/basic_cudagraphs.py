from nemo.core.utils.cuda_python_utils import (
    my_torch_cond,
)

import torch
from torch._C import DispatchKey
from torch._higher_order_ops.cond import cond_op
# TODO: Move this definition to pytorch.
cond_op.py_kernels[DispatchKey.CompositeExplicitAutograd] = my_torch_cond

def simple_conditional_op(pred: torch.Tensor, a: torch.Tensor, b: torch.Tensor):
    return torch.cond(pred, lambda x, y: x + y, lambda x, y: x * y, (a, b))

# We might need to make sure that this will 
compiled_simple_conditional_op = torch.compile(simple_conditional_op, backend="cudagraphs") # mode="reduce-overhead")  # backend="cudagraphs")

a = torch.tensor([1.0], device="cuda")
b = torch.tensor([2.0], device="cuda")

pred = torch.tensor(True, device="cuda")

torch.cuda.cudart().cudaProfilerStart()
for i in range(10):
    torch.cuda.nvtx.range_push(f"iteration = {i}")
    torch.compiler.cudagraph_mark_step_begin()
    c = compiled_simple_conditional_op(pred, a, b)
    print(i)
    print(c)
    torch.cuda.nvtx.range_pop()
torch.cuda.cudart().cudaProfilerStop()
