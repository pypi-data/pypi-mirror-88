import argparse
import sys

import tensorflow as tf
import tensorflow_datasets as tfds
import numpy as np

from onnxds import datasets_pb2
from onnx import onnx_pb2

def tfwrite_ds(ox: datasets_pb2.Dataset, ds: tf.data.Dataset):
    for el in ds:
        tfwrite_ds_iterator(ox.iters.add(), el)

def tfwrite_ds_iterator(ox: datasets_pb2.DatasetIter, el: any):
    if isinstance(el, dict):
        for key in el:
            tfwrite_ds_entry(ox.dicts.dicts[key], el[key])
    else:
        tfwrite_ds_entry(ox.entry, el)

def tfwrite_ds_entry(ox: datasets_pb2.DatasetEntry, el: any):
    if isinstance(el, tf.Tensor):
        tfwrite_tensor(ox.tensor, el)
    elif isinstance(el, tf.data.Dataset):
        tfwrite_ds(ox.dataset, el)
    else:
        assert('unhandled type {}'.format(type(el)))

def tfwrite_tensor(ox: onnx_pb2.TensorProto, tens: tf.Tensor):
    data = tens.numpy()
    shape = data.shape

    if data.dtype == np.int8:
        dtype = onnx_pb2.TensorProto.DataType.INT8
    elif data.dtype == np.uint8:
        dtype = onnx_pb2.TensorProto.DataType.UINT8
    elif data.dtype == np.int16:
        dtype = onnx_pb2.TensorProto.DataType.INT16
    elif data.dtype == np.uint16:
        dtype = onnx_pb2.TensorProto.DataType.UINT16
    elif data.dtype == np.int32:
        dtype = onnx_pb2.TensorProto.DataType.INT32
    elif data.dtype == np.uint32:
        dtype = onnx_pb2.TensorProto.DataType.UINT32
    elif data.dtype == np.int64:
        dtype = onnx_pb2.TensorProto.DataType.INT64
    elif data.dtype == np.uint64:
        dtype = onnx_pb2.TensorProto.DataType.UINT64
    elif data.dtype == np.single:
        dtype = onnx_pb2.TensorProto.DataType.FLOAT16
    elif data.dtype == np.double:
        dtype = onnx_pb2.TensorProto.DataType.DOUBLE
    else:
        dtype = onnx_pb2.TensorProto.DataType.UNDEFINED
    ox.dims.extend(shape)
    ox.data_type = dtype
    if dtype in (
        onnx_pb2.TensorProto.DataType.INT8,
        onnx_pb2.TensorProto.DataType.UINT8,
        onnx_pb2.TensorProto.DataType.INT16,
        onnx_pb2.TensorProto.DataType.UINT16,
        onnx_pb2.TensorProto.DataType.INT32):
        ox.int32_data.extend(data.flatten())
    elif dtype == onnx_pb2.TensorProto.DataType.INT64:
        ox.int64_data.extend(data.flatten())
    elif dtype in (
        onnx_pb2.TensorProto.DataType.UINT32,
        onnx_pb2.TensorProto.DataType.UINT64):
        ox.uint64_data.extend(data.flatten())
    elif dtype in (
        onnx_pb2.TensorProto.DataType.FLOAT16,
        onnx_pb2.TensorProto.DataType.DOUBLE):
        ox.float_data.extend(data.flatten())
    else:
        raw = data.flatten()
        if isinstance(raw[0], bytes) or isinstance(raw[0], str):
            ox.data_type = onnx_pb2.TensorProto.DataType.STRING
            ox.string_data.extend(raw)
        else:
            assert False, 'failed to serialize unknown datatype {}: {}...'.format(type(raw[0]), raw[0])

def tfgen_model(name: str, fname = None, **kwargs):
    ox_ds = datasets_pb2.Dataset()
    tf_ds = tfds.load(name, **kwargs)
    tfwrite_ds(ox_ds, tf_ds)
    if fname is None:
        fname = '/tmp/{}.onnx'.format(name)
    with open(fname, "wb") as f:
        f.write(ox_ds.SerializeToString())

if __name__ == '__main__':
    prog_description = 'Convert tensorflow dataset to onnx dataset'
    parser = argparse.ArgumentParser(description=prog_description)
    parser.add_argument('name')
    parser.add_argument('--out', dest='out',
        type=str, nargs='?', default=None,
        help='Filename to generate onnx dataset')
    parser.add_argument('--split', dest='split',
        type=str, nargs='?', default=None,
        help='Tfds.Split subset: one of TRAIN, VALIDATION, TEST, or any other option uses default')
    parser.add_argument('--batch', dest='batch',
        type=int, nargs='?', default=1,
        help='Tfds batch argument')
    args = parser.parse_args(sys.argv[1:])

    argvs = {
        'batch_size': args.batch
    }
    if args.split == 'TRAIN':
        argvs['split'] = tfds.Split.TRAIN
    elif args.split == 'VALIDATION':
        argvs['split'] = tfds.Split.VALIDATION
    elif args.split == 'TEST':
        argvs['split'] = tfds.Split.TEST
    tfgen_model(args.name, fname=args.out, **argvs)
