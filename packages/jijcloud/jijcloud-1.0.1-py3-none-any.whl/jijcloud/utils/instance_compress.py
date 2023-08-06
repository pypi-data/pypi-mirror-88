import json
import base64
import zstandard as zstd

def encode_instance(problem):
    cctx = zstd.ZstdCompressor()
    encoded_problem = {'instance_type': problem['instance_type']}
    encoded_problem['encoded_instance'] = base64.b64encode(cctx.compress(json.dumps(problem['instance']).encode('utf-8'))).decode('ascii')
    return encoded_problem

def decode_instance(encoded_problem):
    dctx = zstd.ZstdDecompressor()
    problem = {'instance_type': encoded_problem['instance_type']}
    problem['instance'] = json.loads(dctx.decompress(base64.b64decode(encoded_problem['encoded_instance'].encode('ascii'))).decode('utf-8'))
    return problem
