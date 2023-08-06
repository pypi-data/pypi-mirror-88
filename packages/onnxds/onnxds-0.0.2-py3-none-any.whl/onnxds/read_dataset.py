import numpy as np

from onnxds import datasets_pb2
from onnx import onnx_pb2

def load(filename: str):
    with open(filename, 'rb') as f:
        ds = datasets_pb2.Dataset()
        ds.ParseFromString(f.read())
        return read_ds(ds)
    return None

def read_ds(ds: datasets_pb2.Dataset):
    for it in ds.iters:
        ds_iter = read_ds_iterator(it)
        yield ds_iter

def read_ds_iterator(it: datasets_pb2.DatasetIter):
    if it.HasField('entry'):
        return read_ds_entry(it.entry)
    elif it.HasField('dicts'):
        dicts = it.dicts.dicts
        return dict([(k, read_ds_entry(dicts[k])) for k in dicts])
    else:
        raise 'no entry or dicts for DatasetIter'

def read_ds_entry(entry: datasets_pb2.DatasetEntry):
    if entry.HasField('tensor'):
        return read_ds_tensor(entry.tensor)
    elif entry.HasField('dataset'):
        return read_ds(entry.dataset)
    else:
        raise 'no tensor or dataset for DatasetEntry'

_onnx_type_match = {
    onnx_pb2.TensorProto.DataType.INT8: np.int8,
    onnx_pb2.TensorProto.DataType.UINT8: np.uint8,
    onnx_pb2.TensorProto.DataType.INT16: np.int16,
    onnx_pb2.TensorProto.DataType.UINT16: np.uint16,
    onnx_pb2.TensorProto.DataType.INT32: np.int32,
    onnx_pb2.TensorProto.DataType.UINT32: np.uint32,
    onnx_pb2.TensorProto.DataType.INT64: np.int64,
    onnx_pb2.TensorProto.DataType.UINT64: np.uint64,
    onnx_pb2.TensorProto.DataType.FLOAT16: np.single,
    onnx_pb2.TensorProto.DataType.DOUBLE: np.double,
    onnx_pb2.TensorProto.DataType.STRING: np.object
}

def read_ds_tensor(tensor: onnx_pb2.TensorProto):
    assert tensor.data_type != onnx_pb2.TensorProto.DataType.UNDEFINED and\
        tensor.data_type in _onnx_type_match,\
        'unsupported or unknown tensor data type {}'.format(tensor.data_type)
    shape = tensor.dims
    dtype = _onnx_type_match[tensor.data_type]
    raw = []
    if tensor.data_type in (
        onnx_pb2.TensorProto.DataType.INT8,
        onnx_pb2.TensorProto.DataType.UINT8,
        onnx_pb2.TensorProto.DataType.INT16,
        onnx_pb2.TensorProto.DataType.UINT16,
        onnx_pb2.TensorProto.DataType.INT32):
        raw = tensor.int32_data
    elif tensor.data_type == onnx_pb2.TensorProto.DataType.INT64:
        raw = tensor.int64_data
    elif tensor.data_type in (
        onnx_pb2.TensorProto.DataType.UINT32,
        onnx_pb2.TensorProto.DataType.UINT64):
        raw = tensor.uint64_data
    elif tensor.data_type in (
        onnx_pb2.TensorProto.DataType.FLOAT16,
        onnx_pb2.TensorProto.DataType.DOUBLE):
        raw = tensor.float_data
    elif tensor.data_type == onnx_pb2.TensorProto.DataType.STRING:
        raw = tensor.string_data
    return np.array(raw, dtype=dtype).reshape(shape)
